import json
import logging
import math
import os
import time

from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver

from src.SeleniumTorWebDriver import SeleniumTorWebDriver
from src.prices.dns.Products import Products

class ProductsParser:
    def __init__(self, 
                 logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        selenium_manager = SeleniumTorWebDriver(logger=logger)
        self.selenium_manager = selenium_manager
        self.web_driver = self.selenium_manager.get_driver(True)

        self.link = None

    # реакция при окончании работы или возникновение ошибки
    def __exit__(self, exc_type, exc_value, traceback):
        if self.link != None:
            self.logger.info(f"Работа парсера завершена, lint: {self.link}")

        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self

    def get_html(self, link: str):
        retries = 0
        while retries < 5:
            self.web_driver.get(link)

            script_presence = WebDriverWait(self.web_driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "footer"))
            )

            if self.web_driver.title == "HTTP 403":
                self.logger.info(f"Link: {link}. title = HTTP 403")
                self.selenium_manager.remove_port(self.selenium_manager.current_port)
                self.web_driver = self.selenium_manager.get_driver(True)
                continue

            html = self.web_driver.page_source

            if html == None or len(html) == 0:
                self.logger.info(f"Link: {link}. html = None")
                self.selenium_manager.remove_port(self.selenium_manager.current_port)
                self.web_driver = self.selenium_manager.get_driver(True)
                continue

            return html

        self.logger.info(f"Link: {link}. html код = None.")
        return None
    
    def get_product_data(self, link: str):
        html = self.get_html(link)

        # найти uid
        # код производителя
        # цена
        # в наличии (что написано)
        # город

        # if не комплектующие для пк
        # то нахуй этот элеменТ

    def get_all_data(self):
        products = Products()
        links = products.get_links_to_parse_from_json()

        for category, link in links.items():
            html = self.get_html(link)




    
# 1. алгоритм сбора uid + код комплектующей
# 2. через microdata собираем цены
    
# https://www.dns-shop.ru/sitemap.xml, https://www.dns-shop.ru/products1.xml
# https://www.dns-shop.ru/product/microdata/uid/
# https://www.dns-shop.ru/product/microdata/c3c60e33-a198-11eb-a250-00155dd2ff18/