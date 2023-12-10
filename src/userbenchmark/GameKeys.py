from ..SeleniumWebDriver import SeleniumWebDriver
from ..TorManager import TorManager

import logging
from logging import Logger

import json
import re
import time

import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

GAMES_LIST_LINK = "https://www.userbenchmark.com/Search?searchTerm=FPS"
LINK_LOADING_WAIT = 15
CHANGE_PAGE_BUTTON_WAIT = 10

# класс для получения названия игр и их ключей
class GameKeys:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        # запуск тора
        self.tor_manager = TorManager(logger)
        while True:
            if self.tor_manager.start_tor() == False:
                continue
            else:
                break

        self.users_with_ports = TorManager.get_users()

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")

        self.tor_manager.close_tor()

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    def __web_driver_quit(web_driver):
        web_driver.delete_all_cookies()
        web_driver.quit()

    # метод получения web driver с прогруженной страницей с GAMES_LISK_LINK
    def __get_web_driver_on_link(self, link):
        while True:
            try:
                port, user = TorManager.get_random_user(self.users_with_ports)

                selenium_driver = SeleniumWebDriver(logger)
                web_driver = selenium_driver.get_web_driver(port, user)
                web_driver.get(link)

                wait = WebDriverWait(web_driver, LINK_LOADING_WAIT)
                wait.until(EC.visibility_of_all_elements_located((By.ID, "searchForm")))
        
                return web_driver
            except TimeoutException:
                GameKeys.__web_driver_quit(web_driver)
                continue
    
    # метод осуществляющий клик на кнопку
    def __pages_button_click(self, web_driver, button_id):
        try:
            more_button = WebDriverWait(web_driver, CHANGE_PAGE_BUTTON_WAIT).until(EC.presence_of_element_located((By.ID, button_id)))

            wait = WebDriverWait(web_driver, CHANGE_PAGE_BUTTON_WAIT)
            wait.until(EC.element_to_be_clickable((By.ID, button_id)))
            more_button.click()

            return True
        except TimeoutException:
            self.logger.error(f"TimeoutException обработана в методе get_game_links_from_all_pages.")
            GameKeys.__web_driver_quit(web_driver)

            return False

    # метод для клика на первой странице (кнопка more_pages)
    def __more_pages_button_click(self, web_driver):
        try:
            web_driver.execute_script("window.scrollTo(0, 500);")
            more_button_id = "searchForm:j_idt61"
            return self.__pages_button_click(web_driver, more_button_id)
        except TimeoutException:
            self.logger.error(f"TimeoutException обработана в методе get_game_links_from_all_pages.")
            GameKeys.__web_driver_quit(web_driver)

            return False
    
    # метод для ожидания прогрузки страницы
    def __wait_to_page_load(self, web_driver):
        try:
            disabled_li_element_class_name = "disabled"
            wait = WebDriverWait(web_driver, CHANGE_PAGE_BUTTON_WAIT)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, disabled_li_element_class_name)))
        except TimeoutException:
            self.logger.error(f"TimeoutException обработана в методе __wait_to_page_load.")
            GameKeys.__web_driver_quit(web_driver)

            return False
        
        return True

    # метод для получения кол-ва страниц с играми
    def __get_pages_count(self, web_driver):
        try:
            if self.__wait_to_page_load(web_driver) == False:
                return None

            disabled_li_element = web_driver.find_element(By.CLASS_NAME, 'disabled')
        except TimeoutException:
            self.logger.error(f"TimeoutException обработана в методе __get_pages_count.")
            GameKeys.__web_driver_quit(web_driver)

            return None
        
        # gets pages count from element
        text = disabled_li_element.text.strip()
        words = text.split()
        pages_count = 0
        if len(words) > 0:
            pages_count = words[-1]

        return pages_count

    # получение ссылок на игры с одной страницы
    def __get_game_links_from_page(self, web_driver):
        link_element_class_name = "tl-tag"
        disabled_li_element_class_name = "disabled"

        try:
            wait = WebDriverWait(web_driver, CHANGE_PAGE_BUTTON_WAIT)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, disabled_li_element_class_name)))

            links_elements = web_driver.find_elements(By.CLASS_NAME, link_element_class_name)

            links = []
            for link_element in links_elements:
                if link_element:
                    link = link_element.get_attribute("href")
                    if link:
                        links.append(link)

        except TimeoutException:
            self.logger.error(f"TimeoutException обработана в методе __get_game_links_from_page.")
            GameKeys.__web_driver_quit(web_driver)
            return []
        except StaleElementReferenceException:
            self.logger.error(f"StaleElementReferenceException обработана в методе __get_game_links_from_page.")
            GameKeys.__web_driver_quit(web_driver)
            return []

        return links

    # метод для клика кнопки для перехода на следующую страницу
    def __next_page_button_click(self, web_driver):
        try:
            web_driver.execute_script("window.scrollTo(0, 10000);")
            next_page_button_id = "searchForm:j_idt80"
            if self.__pages_button_click(web_driver, next_page_button_id) == False:
                return False
            
            if self.__wait_to_page_load(web_driver) == False:
                return False
        except TimeoutException:
            self.logger.error(f"TimeoutException обработана в методе __next_page_button_click.")
            GameKeys.__web_driver_quit(web_driver)

            return False
        
        return True
    
    # получение игровых ключей из ссылки
    def __extract_game_keys_from_links(self, links):
        game_keys_data = {}
        for link in links:
            game_id = re.search(r'/(\d+)/', link).group(1)
            game_title = re.search(r'\/([^/]+)/(\d+)/', link).group(1).replace("FPS-Estimates-", "").replace('--', ' ').replace('-', ' ').rstrip()
            game_keys_data[game_id] = game_title

        return game_keys_data
    
    # получение всех ссылок на игры
    def get_game_links_from_all_pages(self):
        while True:
            web_driver = self.__get_web_driver_on_link(GAMES_LIST_LINK)

            if self.__more_pages_button_click(web_driver) == False:
                continue

            pages_count = self.__get_pages_count(web_driver)
            if pages_count == None:
                continue

            # gets links from all pages
            links = []
            for i in range(int(pages_count)):
                if (i == int(pages_count) - 1):
                    links = links + self.__get_game_links_from_page(web_driver)
                    web_driver.delete_all_cookies()
                    web_driver.quit()
                    break

                links = links + self.__get_game_links_from_page(web_driver)
                
                if self.__next_page_button_click(web_driver) == False:
                    continue

                time.sleep(1)

            # remove last game link, cause error on web site
            links.pop()
            game_keys_data = self.__extract_game_keys_from_links(links)

            return game_keys_data

    # получение ключей из json
    def get_game_keys_from_json():
        current_directory = os.getcwd()
        file_path = current_directory + "\\data\\userbenchmark\\game_keys.json"

        with open(file_path, 'r', encoding='utf-8') as json_file:
            game_keys = json.load(json_file)
            
        return game_keys
    
    # сохранение ключей в json
    def save_game_keys_to_json(game_keys):
        current_directory = os.getcwd()
        file_path = current_directory + "\\data\\userbenchmark\\game_keys.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(game_keys, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        encoding='utf-8')
    logger = logging.getLogger("userbenchmark_game_keys_parser")
    file_handler = logging.FileHandler("userbenchmark_parser\\logs\\userbenchmark_game_keys_parser.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    parser = GameKeys(logger)
    with parser:
        game_keys_data = parser.get_game_links_from_all_pages()
        GameKeys.save_game_keys_to_json(game_keys_data)