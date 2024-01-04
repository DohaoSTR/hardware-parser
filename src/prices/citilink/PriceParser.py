import json
import logging
import math
import os
import time

from datetime import datetime
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchWindowException

from src.SeleniumTorWebDriver import SeleniumTorWebDriver

HEADLESS = True
IS_IMAGES_LOAD = True

class PriceParser:
    def __init__(self, 
                 logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        selenium_manager = SeleniumTorWebDriver(logger=logger)
        self.selenium_manager = selenium_manager

        self.web_driver = self.selenium_manager.get_driver(IS_IMAGES_LOAD, HEADLESS)
        
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
            self.logger.info("Окно уже закрыто.")

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self

    def __parse_html_content(self, 
                           link: str):
        retries = 0
        while retries < 5:
            try:
                self.web_driver.get(link)

                time.sleep(3)

                self.web_driver.execute_script("window.scrollBy(0, 500);")
                
                if self.web_driver.title == "Ошибка 404: страница не найдена":
                    self.logger.info(f"Link: {link}. Ошибка 404: страница не найдена.")
                    self.selenium_manager.clear_web_drivers(self.web_driver)
                    self.web_driver = self.selenium_manager.get_driver(IS_IMAGES_LOAD, HEADLESS)
                    continue

                if self.web_driver.title == "429":
                    self.logger.info(f"Link: {link}. Ошибка 429. Слишком частые запросы.")
                    self.selenium_manager.clear_web_drivers(self.web_driver)
                    self.web_driver = self.selenium_manager.get_driver(IS_IMAGES_LOAD, HEADLESS)
                    continue

                if self.web_driver.title == "":
                    self.logger.info(f"Link: {link}. title == 0")
                    self.selenium_manager.clear_web_drivers(self.web_driver)
                    self.web_driver = self.selenium_manager.get_driver(IS_IMAGES_LOAD, HEADLESS)
                    continue

                html = self.web_driver.page_source
                
                if html == None or len(html) == 0:
                    self.logger.info(f"Link: {link}. title == 0")
                    self.selenium_manager.clear_web_drivers(self.web_driver)
                    self.web_driver = self.selenium_manager.get_driver(IS_IMAGES_LOAD, HEADLESS)
                    continue
                
                return html
            except TimeoutException as e:
                self.logger.info(f"Link: {link}. TimeoutException - {e}")
                continue
        
        self.logger.info(f"Link: {link}. html код = None.")
        return None
    
    def parse_pages_count(self,
                        html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        count_element = soup.find('span', {'data-meta-name': 'SubcategoryPageTitle__product-count'})

        if count_element == None:
            return None
        
        count = count_element.get('data-meta-product-count')
        pages_count = math.ceil(int(count) / 48)
        
        return pages_count
    
    def parse_page_data(self, 
                      html_content: str, 
                      city_name: str,
                      category: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        product_elements = soup.find_all('div', {'data-meta-name': 'ProductHorizontalSnippet'})
        product_elements += soup.find_all('div', {'data-meta-name': 'ProductVerticalSnippet'})

        if len(product_elements) == 0:
            self.logger.info(f"Длина - {len(product_elements)}")

        data = []
        for product_element in product_elements:
            price_element = product_element.find(attrs={"data-meta-price": True})
            
            if price_element != None:
                price = price_element.get('data-meta-price')
                available = True
            else:
                price = None
                available = False

            title_element = product_element.find('a', class_ = "app-catalog-9gnskf e1259i3g0")
            if title_element == None:
                a_element = product_element.find('a', class_ = "app-catalog-1k0cnlg e1mnvjgw0")
                link = "https://www.citilink.ru/" + a_element.get('href')

                title_element = a_element.find('span')
                if title_element != None:
                    title = title_element.text
                else:
                    image_tag = soup.find('img')
                    title = image_tag['alt']
            else:
                link = "https://www.citilink.ru/" + title_element.get('href')
                title = title_element.get('title')

            data.append({
                "title": title,
                "link": link,
                "price": price,
                "available": available,
                "city_name": city_name,
                "category": category,
                "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return data
    
    def get_link(self,
                 category_link: str,
                 page_number: int,
                 city_code: str):
        link = category_link + f"?p={page_number}&action=changeCity&space={city_code}"
        
        return link

    def parse_category_data(self, 
                          category_link: str,
                          category_name: str,
                          city_code: str,
                          city_name: str):
        self.link = self.get_link(category_link, 1, city_code)

        while True:
            html_content = self.__parse_html_content(self.link)
            first_page_data = self.parse_page_data(html_content, city_name, category_name)
            pages_count = self.parse_pages_count(html_content)

            if pages_count == None:
                continue
            else:
                break

        data = first_page_data
        for page_number in range(2, pages_count):
            while True:
                self.link = self.get_link(category_link, page_number, city_code)
                html_content = self.__parse_html_content(self.link)
                try:
                    page_data = self.parse_page_data(html_content, city_name, category_name)
                except AttributeError as e:
                    self.logger.info(f"Link: {self.link}. AttributeError")
                    continue

                if page_data == None or len(page_data) == 0:
                    continue
                else:
                    data += page_data
                    self.logger.info(f"Link: {self.link}. Длина page_data - {len(page_data)}.")
                    self.logger.info(f"Link: {self.link}. page_data[0] - {page_data[0]}.")
                    break

        return data

    def get_data(self):
        current_directory = os.getcwd()
        path = current_directory + "\\data\\prices\\citilink\\prices.json"

        try:
            with open(path, 'r', encoding="utf-8") as file:
                prices_data = json.load(file)
        except FileNotFoundError:
            return None

        return prices_data

    def auto_save_data(self, data):
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
        path = current_directory + "\\data\\prices\\citilink\\prices.json"
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(sorted_data, json_file, indent=4, ensure_ascii=False)

    def save_data(self, data):
        sorted_data = {}
        index = 0
        for item in data:
            sorted_data[index] = item
            index += 1

        current_directory = os.getcwd()
        path = current_directory + "\\data\\prices\\citilink\\prices.json"
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(sorted_data, json_file, indent=4, ensure_ascii=False)

    def parse_all_data(self):
        current_directory = os.getcwd()
        categories_path = current_directory + "\\data\\prices\\citilink\\categories_to_parse.json"
        with open(categories_path, 'r', encoding="utf-8") as file:
            categories_data = json.load(file)

        city_codes_path = current_directory + "\\data\\prices\\citilink\\city_codes.json"
        with open(city_codes_path, 'r', encoding="utf-8") as file:
            city_codes_data = json.load(file)

        data = []
        for category_name, category_link in categories_data.items():
            for city_name, city_code in city_codes_data.items():
                data += self.parse_category_data(category_link, 
                                                       category_name, 
                                                       city_code, 
                                                       city_name)
        self.save_data(data)
        return data