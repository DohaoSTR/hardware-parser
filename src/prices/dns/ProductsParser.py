from datetime import datetime

import json
import logging
import os
import re
import time

from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchWindowException

from src.SeleniumTorWebDriver import SeleniumTorWebDriver
from src.prices.dns.Products import Products

ELEMENT_CLASS = "ui-link"
ELEMENT_TEXT = "Комплектующие для ПК"

HEADLESS_BROWSER = False
IMAGES_LOAD = False

MICRODATA_LINK = "https://www.dns-shop.ru/product/microdata/"

WAIT_HTML_CONTENT_LOAD = 1

# мб оптимизировать процесс запуска tor и проверок

# дописать алгоритм парсинга цены по uid и переноса в бд
# дописать алгоритм переноса в бд характерстик (необходимых)
# алгоритм парсинга наличия и переноса наличия в бд
class ProductsParser:
    def __init__(self, 
                 logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        selenium_manager = SeleniumTorWebDriver(logger=logger)
        self.selenium_manager = selenium_manager

        self.web_driver = self.selenium_manager.get_driver(IMAGES_LOAD, HEADLESS_BROWSER)
        self.link = None

    # реакция при окончании работы или возникновение ошибки
    def __exit__(self, exc_type, exc_value, traceback):
        if self.link != None:
            self.logger.info(f"Работа парсера завершена, lint: {self.link}")

        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")

        try:
            if self.web_driver != None:
                self.selenium_manager.clear_web_drivers(self.web_driver)
        except NoSuchWindowException:
            print("Окно уже закрыто.")

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self

    def __get_html_content(self, link: str):
        retries = 0
        while retries < 5:
            try:
                try:
                    self.web_driver.get(link)
                except TimeoutException:
                    self.logger.info(f"Link: {link}. (0) TimeoutException")
                    continue

                while True:
                    try:
                        wait = WebDriverWait(self.web_driver, WAIT_HTML_CONTENT_LOAD)

                        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "product-characteristics__spec-title")))
                        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "product-characteristics__spec-value")))
                        self.logger.info(f"Link: {link}. Timeout True")
                        break
                    except TimeoutException:
                        self.logger.info(f"Link: {link}. TimeoutException")

                        if self.web_driver.title == "HTTP 403":
                            self.logger.info(f"Link: {link}. title (1) = HTTP 403")
                            break

                        continue
                
                if self.web_driver.title == "HTTP 403":
                    self.logger.info(f"Link: {link}. title (2) = HTTP 403")
                    self.selenium_manager.clear_web_drivers(self.web_driver)
                    self.web_driver = self.selenium_manager.get_driver(IMAGES_LOAD, HEADLESS_BROWSER)
                    continue

                self.web_driver.execute_script("window.scrollBy(0, 500);")

                html = self.web_driver.page_source
                if html == None or len(html) == 0:
                    self.logger.info(f"Link: {link}. html = None")
                    self.selenium_manager.clear_web_drivers(self.web_driver)
                    self.web_driver = self.selenium_manager.get_driver(IMAGES_LOAD, HEADLESS_BROWSER)
                    continue

            except NoSuchWindowException:
                self.logger.info(f"Link: {link}. NoSuchWindowException")
                self.web_driver = self.selenium_manager.get_driver(IMAGES_LOAD, HEADLESS_BROWSER)
                continue

            return html

        self.logger.info(f"Link: {link}. html код = None.")
        return None
    
    def __is_necessary_product(self, html_content: str) -> bool:
        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.find('a', class_=ELEMENT_CLASS, text=ELEMENT_TEXT)
        if element:
            return True
        else:
            self.logger.info(f"Элемент с классом '{ELEMENT_CLASS}' и текстом '{ELEMENT_TEXT}' не найден.")
            return False

    def __get_uid(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        scripts = soup.find_all('script')

        cardMicrodataUrl = None
        for script in scripts:
            script_content = script.string
            if script_content and 'window.cardMicrodataUrl' in script_content:
                match = re.search(r'window\.cardMicrodataUrl\s*=\s*[\'"]([^\'"]+)[\'"]', script_content)
                
                if match and match.group(1):
                    cardMicrodataUrl = match.group(1)
                    cardMicrodataUrl = cardMicrodataUrl.split("/")[3]
                else:
                    self.logger.info(f"Link: {self.link}. Не удалось извлечь значение window.cardMicrodataUrl")

                break

        return cardMicrodataUrl

    def __get_availability_status(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        element = soup.find('div', class_='order-avail-wrap')

        if element == None:
            raise AttributeError("div.order-avail-wrap == None")

        element_a = element.find('a')
        if element_a == None:
            return element.text
        else:
            return element_a.text

    def __get_specs(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')  
        title_divs = soup.find_all('div', class_='product-characteristics__spec-title')

        specs = []
        for title_div in title_divs:
            value_div = title_div.find_next_sibling('div', class_='product-characteristics__spec-value')
            specs.append({
                "Name": title_div.text.strip(),
                "Value": value_div.text.strip()
            })

        return specs

    #"date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def get_product_data(self, link: str):
        while True:
            self.link = link + "characteristics/"
            html_content = self.__get_html_content(self.link)

            try:
                if self.__is_necessary_product(html_content) == False:
                    return None
                
                uid = self.__get_uid(html_content)
                specs = self.__get_specs(html_content)

                return {
                    "link": link,
                    "uid": uid,
                    "specs": specs
                }
            except AttributeError as e:
                self.logger.info(f"Link: {link}. AttributeError")
                continue
    
    def get_data(self):
        current_directory = os.getcwd()
        path = current_directory + "\\data\\prices\\dns\\products.json"

        try:
            with open(path, 'r', encoding="utf-8") as file:
                prices_data = json.load(file)
        except FileNotFoundError:
            return None

        return prices_data
    
    def save_data(self, data):
        prices_data = self.get_data()

        if prices_data == None:
            existing_data = {}
        else:
            existing_data = prices_data

        sorted_data = {}
        index = 0
        for key, value in existing_data.items():
            sorted_data[index] = value
            index += 1

        for item in data:
            sorted_data[index] = item
            index += 1
    
        current_directory = os.getcwd()
        path = current_directory + "\\data\\prices\\dns\\products.json"
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(sorted_data, json_file, indent=4, ensure_ascii=False)

    def get_all_data(self):
        links = self.get_links_from_last_link()

        if links == None or len(links) == 0:
            return

        data = []
        for index, item in links.items():
            product_data = self.get_product_data(item["link"])
            if product_data != None:
                product_data["category"] = item["category"]
                data.append(product_data)

            if int(index) % 10 == 0:
                self.save_data(data)
                data = []

    def get_last_link_from_products(self):
        products = self.get_data()

        if products == None:
            return None

        last_item_key = max(products, key=lambda x: int(x))
        last_item = products[last_item_key]

        return last_item["link"]

    def get_links_from_last_link(self):
        products = Products()
        links = products.get_links_to_parse_from_json()

        last_link = self.get_last_link_from_products()
        if last_link == None:
            return links
        
        for index, item in links.items():
            if item["link"] == last_link:
                return {k: v for k, v in links.items() if int(k) >= int(index) + 1}


    ###
    def get_status_data(self):
        pass
    
    # метод для получения ссылок для получения статусов
    def get_links_to_status_parse(self):
        pass

    def get_all_status(self):
        products = Products()
        links = products.get_links_to_parse_from_json()

        if links == None or len(links) == 0:
            return

        data = []
        for index, item in links.items():
            product_data = self.get_status_data(item["link"])
            if product_data != None:
                product_data["category"] = item["category"]
                data.append(product_data)

            if int(index) % 10 == 0:
                self.save_data(data)
                data = []
    ###


    ###
    def get_products_uid(self):
        data = self.get_data()

        for index, item in data.items():
            link = item["link"]
            uid = item["uid"]

            link

    # быстрое обновление цен через microdata
    def get_price(self, uid: str):
        self.link = MICRODATA_LINK + uid + "/"
        pass
    ###
    
    # полное обновление данных с переносом в бд
    def refresh_all_data_mapper(self):
        pass

# https://www.dns-shop.ru/product/microdata/uid/
# https://www.dns-shop.ru/product/microdata/c3c60e33-a198-11eb-a250-00155dd2ff18/