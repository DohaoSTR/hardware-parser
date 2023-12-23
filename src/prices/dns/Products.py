import json
import logging
import math
import os
import time

from bs4 import BeautifulSoup
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver

from src.SeleniumTorWebDriver import SeleniumTorWebDriver

import xml.etree.ElementTree as ET

xml_links = [
    "https://www.dns-shop.ru/products1.xml",
    "https://www.dns-shop.ru/products2.xml",
    "https://www.dns-shop.ru/products3.xml"
]

class Products:
    def __init__(self, 
                 logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        #selenium_manager = SeleniumTorWebDriver(logger=logger)
        #self.selenium_manager = selenium_manager
        #self.web_driver = self.selenium_manager.get_driver(True)

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

    def save_all_links(self):
        current_directory = os.getcwd()
        path = current_directory + "\\data\\prices\\dns\\"

        index = 1
        for xml_link in xml_links:
            response = requests.get(xml_link)

            if response.status_code == 200:
                with open(path + "products" + str(index), 'wb') as file:
                    file.write(response.content)
            else:
                print(f"Ошибка при скачивании файла. Код статуса: {response.status_code}")

            index += 1

    def get_all_links(self):
        current_directory = os.getcwd()
        path = current_directory + "\\data\\prices\\dns\\"

        data = []
        for number in range(1, len(xml_links) + 1): 
            tree = ET.parse(path + "products" + str(number))
            root = tree.getroot()
            namespaces = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            urls = [url_element.text for url_element in root.findall(".//ns:loc", namespaces)]
            data += urls

        return data

    def get_links_to_parse(self):
        links = self.get_all_links()

        current_directory = os.getcwd()
        path = current_directory + "\\data\\prices\\dns\\categories_to_parse.json"
        with open(path, 'r', encoding="utf-8") as file:
            categories_to_parse = json.load(file)

        links_to_parse = {}
        index = 0
        for link in links:
            for category, dns_category in categories_to_parse.items():
                if str(link).__contains__(dns_category) == True:
                    links_to_parse[index] = { "category": category, "link": link }
                    index += 1
                    break

        return links_to_parse

    def save_parts_links(self):
        links_to_parse = self.get_links_to_parse()

        current_directory = os.getcwd()
        path = current_directory + "\\data\\prices\\dns\\links_to_parse.json"
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(links_to_parse, json_file, indent=4, ensure_ascii=False)

    def get_links_to_parse_from_json(self):
        current_directory = os.getcwd()
        path = current_directory + "\\data\\prices\\dns\\links_to_parse.json"

        with open(path, 'r', encoding="utf-8") as file:
            links_to_parse = json.load(file)

        return links_to_parse