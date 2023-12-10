from .Part import Part

from ..cloudflare_bypass.CloudflareTorDriver import CloudflareTorDriver

import logging
from logging import Logger

import json
import os

from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

HTML_PRODUCT_PAGE_RETRIES = 5
HTML_PRODUCT_PAGE_WAIT = 5

LINKS_RELATIVE_PATH = "\\data\\pcpartpicker\\links\\"

# класс для получения ссылок комплектующих с сайта PcPartPicker
class Links:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        self.link = None
        self.web_driver = None
        self.cloudflare_tor_driver = CloudflareTorDriver(self.logger)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.logger is not None:
            self.logger.info(f"Работа парсера завершена, Link: {self.link}")

            self.logger.info("Параметры метода __exit__:")
            self.logger.info(f"Тип возникшего исключения: {exc_type}")
            self.logger.info(f"Значение исключения: {exc_value}")
            self.logger.info(f"Объект traceback: {traceback}")

        self.clear_web_driver()
        
        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    # получение всех ссылок с страницы
    def __get_links_from_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        product_elements = soup.find_all('tr', class_='tr__product')

        links = []
        for product_element in product_elements:
            link_element = product_element.find('a')

            if link_element:
                link = "https://pcpartpicker.com" + link_element['href']
                links.append(link)

        if len(links) == 0:
            return None

        return links

    # получение html кода с страницы product page (страница с комплектующими)
    def __get_html_from_products_page(self, link):
        retries = 0
        while retries < HTML_PRODUCT_PAGE_RETRIES:
            if self.web_driver.title == "Unavailable":
                return None
            try:
                WebDriverWait(self.web_driver, HTML_PRODUCT_PAGE_WAIT).until(
                    EC.visibility_of_element_located((By.TAG_NAME, "tr"))
                )
            except TimeoutException:
                retries = retries + 1
                self.logger.error(f"Link: {link}. TimeoutException обработана на этапе прогрузки страницы с tr__product.")
                continue
            
            html = self.web_driver.page_source

            return html
        
        self.logger.info(f"Link: {link}. html код = None")
        return None

    # полная очистка ресурсов web driver-а
    def clear_web_driver(self):
        self.cloudflare_tor_driver.clear_web_drivers(self.web_driver)
        self.web_driver = None

    # получение ссылок для одной категории комплектующих
    def get_links_of_part(self, part: Part):
        link_without_page = "https://pcpartpicker.com/products/" + part.value + "/"
        links = []

        for page_number in range(1, Part.get_pages_count(part.value) + 1):
            while True:
                link = link_without_page + "#page=" + str(page_number)

                if self.web_driver == None:
                    self.web_driver = self.cloudflare_tor_driver.get_driver(link)
                else:
                    self.web_driver.get(link)
                    if self.cloudflare_tor_driver.check_on_data_page(self.web_driver, link) == False:
                        self.logger.info(f"Link: {link}. Cloudflare страница.")
                        continue
                                            
                html = self.__get_html_from_products_page(link)

                if html == None or len(html) == 0:
                    self.clear_web_driver()
                    continue
                else:
                    returned_links = self.__get_links_from_page(html)
            
                    if returned_links == None or len(returned_links) == 0:
                        self.logger.warning(f"Link: {link}. Получено - 0 ссылок с страницы.")
                        self.clear_web_driver()
                        continue
                    else:
                        returned_links_set = set(returned_links)
                        parsed_links_set = set(links)

                        duplicates = returned_links_set.intersection(parsed_links_set)
                        if len(duplicates) > 0:
                            self.logger.warning(f"Link: {link}. Получены дубликаты ссылок.")
                            continue

                        links = links + returned_links
                        self.logger.info(f"Link: {link}. кол-во ссылок - {len(returned_links)}")
                        break

        self.logger.info(f"Part: {part.value}. кол-во ссылок - {len(links)}")       
        return links

    # сохранение ссылок в json файла
    def save_links_to_json(part: Part, links):
        current_directory = os.getcwd()
        file_path = current_directory + LINKS_RELATIVE_PATH + str(part.value) + "_links.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(links, json_file, indent=4, ensure_ascii=False)

    # получение ссылок из json файла
    def get_links_from_json(part: Part):
        current_directory = os.getcwd()
        file_path = current_directory + LINKS_RELATIVE_PATH + str(part.value) + "_links.json"
        
        with open(file_path, 'r') as json_file:
            links = json.load(json_file)
            
        return links
    
    # получение ссылок для всех категорий комплектующих
    def get_all_links(self):
        for part in Part:
            links = self.get_links_of_part(part)
            Links.save_links_to_json(part, links)