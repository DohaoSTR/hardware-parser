from ..SeleniumWebDriver import SeleniumWebDriver
from ..TorManager import TorManager
from .CloudflareBypass import CaptchaBypasser

import logging
from logging import Logger
import time

import undetected_chromedriver as uc

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

START_PORT = 8000
END_PORT = 9149
PORTS_COUNT_TO_RESTART = 100

TIME_WAIT_AFTER_SOVE_CAPTCHA = 1
CLOUDFLARE_CHECK_RETRIES = 15
CLOUDFLARE_CHECK_WAIT = 1
DATA_CHECK_WAIT = 1

class CloudflareTorDriver:
    def __init__(self, logger: Logger = None, start_port = START_PORT, end_port = END_PORT, ports_count_to_restart = PORTS_COUNT_TO_RESTART):
        self.logger = logger or logging.getLogger(__name__)

        self.tor_manager = TorManager(logger)
        
        while True:
            if self.tor_manager.start_tor() == False:
                continue
            else:
                break

        self.start_port = start_port
        self.end_port = end_port
        self.ports_count_to_restart = ports_count_to_restart

        self.users_with_ports = TorManager.get_users(start_port, end_port)

    # метод для удаления Tor порта
    # при кол-во портов < PORTS_COUNT_TO_RESTART, происходит перезапуск Tor
    def remove_port(self, port):
        if port in self.users_with_ports:
            del self.users_with_ports[port]

            self.logger.info(f"Порт был удалён. Порт: {port}")

            if (len(self.users_with_ports) < PORTS_COUNT_TO_RESTART):
                self.logger.info("Порты кончились.")
                
                self.tor_manager.restart_tor()

                self.users_with_ports = TorManager.get_users(self.start_port, self.end_port)

                self.logger.info("Порты обновлены.")
                
            return True
        else:
            self.logger.warning(f"Порт не найден в списке. Port: {port}")
            return False

    def clear_web_drivers(self, web_driver):
        selenium_web_driver = SeleniumWebDriver(self.logger)
        selenium_web_driver.clear_web_drivers(web_driver)
        
    # метод получения класса webdriver для определенной ссылки
    # данный метод возвращает webdriver с помощью которого уже пройдена
    # cloudflare каптча и создан сеанс работы с сайтом
    def get_driver(self, link):
        while True:
            try:
                port, user_agent = TorManager.get_random_user(self.users_with_ports)

                print(port)
                chrome_options = uc.ChromeOptions()
                chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:' + str(port))
                driver = uc.Chrome(enable_cdp_events=True, options=chrome_options)
                with driver:
                    driver.get(link)

                if self.is_cloudflare(driver, link) == False:
                    self.logger.info(f"Link: {link}. Cloudflare защита пройдена.")
                    return driver
                else:
                    self.clear_web_drivers(driver)
                    continue
            except selenium.common.exceptions.WebDriverException:
                self.logger.error(f"Link: {link}. Ошибка WebDriverException обработана.")
                self.tor_manager.restart_tor()
                self.clear_web_drivers(driver)
                continue
                             
    # метод определяющий является ли страница Cloudflare каптчей
    # или каптча уже пройдена
    # True - каптча пройдена, False - страница все еще Cloudflare
    def is_cloudflare(self, driver, link):
        retries = 0
        while retries < CLOUDFLARE_CHECK_RETRIES:
            try:
                wait = WebDriverWait(driver, CLOUDFLARE_CHECK_WAIT)
                wait.until(EC.presence_of_element_located((By.ID, "challenge-stage")))        
            except TimeoutException:
                self.logger.error(f"Link: {link}. Ошибка TimeoutException обработана. is_cloudflare(1)")
                retries = retries + 1
                continue
            except AttributeError:
                return False

            self.logger.info(f"Link: {link}. Начало решения каптчи.")
            self.__solve_captcha()
            time.sleep(TIME_WAIT_AFTER_SOVE_CAPTCHA)
            self.logger.info(f"Link: {link}. Каптча должна быть решена.")

            try:
                wait = WebDriverWait(driver, DATA_CHECK_WAIT)
                challenge_stage = wait.until(EC.presence_of_element_located((By.ID, "challenge-stage")))
                if challenge_stage:
                    retries = retries + 1
                    continue
                else:
                    self.logger.info(f"Link: {link}. Каптча решена успешно.")
                    return False
            except TimeoutException:
                self.logger.error(f"Link: {link}. Ошибка TimeoutException обработана. is_cloudflare(2)")
                return False
    
        self.logger.info(f"Link: {link}. Страница содержит Cloudflare защиту.")
        return True
    
    # метод проверяющий страницу на наличие данных
    def check_on_data_page(self, driver, link):
        try:
            wait = WebDriverWait(driver, DATA_CHECK_WAIT)
            challenge_stage = wait.until(EC.presence_of_element_located((By.ID, "challenge-stage")))
            if challenge_stage:
                return False
            else:
                self.logger.info(f"Link: {link}. Страница с данными.")
                return True
        except TimeoutException:
            self.logger.error(f"Link: {link}. Ошибка TimeoutException обработана. check_on_data_page")
            return True

    # метод использует класс CloudflareBypass для решения каптчи 
    # каптча решается с помощью нейронной сети
    def __solve_captcha(self):
        captcha_bypasser = CaptchaBypasser(self.logger)
        captcha_bypasser.run()