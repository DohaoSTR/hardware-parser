from .Part import Part
from .Links import Links

from ..cloudflare_bypass.CloudflareTorDriver import CloudflareTorDriver

import logging
from logging import Logger

import json
import re
import os

from datetime import datetime
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

HTML_PRODUCT_PAGE_RETRIES = 15
HTML_PRODUCT_PAGE_WAIT = 1

PARAMETERS_RELATIVE_PATH = "\\data\\pcpartpicker\\parameters\\"

# класс для получения ссылок комплектующих с сайта PcPartPicker
class Parameters:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        self.link = None
        self.web_driver = None
        self.part_id = None

        self.cloudlare_tor_driver = CloudflareTorDriver(self.logger)

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info(f"Работа парсера завершена, Link: {self.link}")

        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")

        self.__clear_web_driver()
        
        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self

    # получение html кода с страницы product page (страница с комплектующими)
    def __get_html_from_products_page(self, link):
        retries = 0
        while retries < HTML_PRODUCT_PAGE_RETRIES:
            if self.web_driver.title == "Unavailable":
                return None
            try:
                WebDriverWait(self.web_driver, HTML_PRODUCT_PAGE_WAIT).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'group'))
                )
            except TimeoutException:
                retries = retries + 1
                self.logger.error(f"Link: {link}. TimeoutException обработана на этапе прогрузки страницы с group.")
                continue
            
            html = self.web_driver.page_source

            return html
        
        self.logger.info(f"Link: {link}. html код = None")
        return None

    # получение названия комплектующей из html
    def __get_name(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1', class_='pageTitle').text

        return title
    
    # получение основных данных о комплектующей
    # { "Header": Название комплектующей }
    # { "PartType": Тип комплектующей } 
    # { "Link": Ссылка на страницу с данными }
    def __get_main_data(self, html: str, link, part: Part):
        name_data = []

        name_data.append({ "Header": "Main" })
        name_data.append({ "Name": self.__get_name(html) })
        name_data.append({ "PartType": part.value })
        name_data.append({ "Link": link })

        link_parts = link.split('/')
        part_code = link_parts[-2]

        name_data.append({ "Key": part_code })

        return name_data, part_code

    # получение данных specification table из html
    # формат одного параметра { "Name": Название параметра, "Value": значение параметра }
    # возвращаемые данные являются характеристиками комплектующей
    def __get_specification_table_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        block = soup.find('div', class_ = "block xs-hide md-block specs")
        elements = block.find_all('div', class_='group')

        table_data = []
        table_data.append({ "Header": "SpecificationTable"})
        
        for element in elements:
            title = element.find('h3', class_='group__title').text.strip()
            content_element = element.find('div', class_='group__content')

            content = None
            if content_element.find('ul'):
                list_items = content_element.find('ul').find_all('li')
                content = [item.text.strip() for item in list_items]
            else:
                content = content_element.text.strip()

            table_data.append({"Name": title, "Value": content})

        return table_data
    
    # метод для получения тэга комплектующей
    def __get_product_tag(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('form', class_='actionBox__formDropdown').find('a', class_='button')

        if element == None:
            return None
        else:
            product_tag = element['data-product-tag']
            return product_tag

    # получение данных user ratings из html
    # формат данных: 
    # { "Name": "RatingsCount", "Value": Кол-во отзывов}
    # { "Name": "AverageRating", "Value": Средний рейтинг}
    # { "Name": "Rating", "Value": Массив значений [ { Уровень оценки (Оценка 5), голосов }, ...]}
    def __get_user_ratings_table_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        div_elements = soup.find_all('div')
        user_ratings_data = []
        user_ratings_data.append({ "Header": "UserRatings"})
        
        for div_element in div_elements:
            user_ratings_element = div_element.find('h6', string="User Ratings")
            if user_ratings_element != None:
                ratings = div_element.find_next('ul', class_='product--rating').text.strip()
                
                ratings_match = re.search(r'(\d+) Ratings', ratings)
                average_match = re.search(r'([\d.]+) Average', ratings)

                if ratings_match:
                    rating_count = int(ratings_match.group(1))
                else:
                    rating_count = None

                if average_match:
                    average_rating = float(average_match.group(1))
                else:
                    average_rating = None

                rating_entries = div_element.find_next('table').find_all('tr')

                rating_data = {}
                for entry in rating_entries:
                    star_rating = entry.find('a', class_='ratingStars').text
                    percentage = entry.find('a', class_='ratingPercentage').text

                    rating_data[star_rating] = percentage

                user_ratings_data.append({ "Name": "RatingsCount", "Value": rating_count})
                user_ratings_data.append({ "Name": "AverageRating", "Value": average_rating})
                user_ratings_data.append({ "Name": "Rating", "Value": rating_data})

                return user_ratings_data

        return user_ratings_data

    # получение данных о ценах (prices tables) из html
    # формат данных: {'MerchantLink': 'https://pcpartpicker.com/mr/gamestop/g94BD3', 'MerchantName': 'GameStop', 
    # 'BasePrice': '$299.00', 'PromoValue': None, 'ShippingText': '+FREE s/h', 'ShippingLink': None, 
    # 'TaxValue': None, 'Availability': 'In stock', 'FinalPrice': '$299.00', 'LastUpdateTime': '2023-10-12 17:24:53'}
    def __get_prices_table_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        price_table = soup.find('div', id='prices').find('table')
        rows = price_table.find_all('tr')

        price_data = []
        price_data.append({ "Header": "PriceData"})

        for row in rows[1:]:
            if "tr--noBorder" in row.get('class', []):
                continue

            td_elements = row.find_all('td')

            merchant_link = None
            merchant_name = None
            base_price = None
            promo_value = None
            shipping_text = None
            shipping_link = None
            tax_value = None
            availability = None
            final_price = None
            
            for td in td_elements:
                class_list = td.get('class', [])

                if "td__logo" in class_list:
                    merchant_link = td.a.get('href')
                    merchant_name = td.a.img.get('alt')

                    if str(merchant_link).startswith("/mr/"):
                        merchant_link = "https://pcpartpicker.com" + merchant_link
                elif "td__base" in class_list:
                    base_price = td.text.strip()
                elif "td__promo" in class_list:
                    promo_value = td.text.strip()
                    if len(promo_value) == 0:
                        promo_value = None
                elif "td__shipping" in class_list:
                    shipping_a = td.a
                    if shipping_a != None:
                        shipping_text = shipping_a.img.get('alt')
                        shipping_link = shipping_a.get('href')
                    else:
                        shipping_text = td.text.strip()
                        if shipping_text == " ":
                            shipping_text = None
                elif "td__tax" in class_list:
                    tax_value = td.text.strip()
                    if len(tax_value) == 0:
                        tax_value = None
                elif "td__availability" in class_list:
                    availability = td.text.strip()
                elif "td__finalPrice" in class_list:
                    final_price = td.a.text.strip()
                else:
                    continue
                
            # получение текущего времени
            current_time = datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

            data_entry = {
                "MerchantLink": merchant_link,
                "MerchantName": merchant_name,
                "BasePrice": base_price,
                "PromoValue": promo_value,
                "ShippingText": shipping_text,
                "ShippingLink": shipping_link,
                "TaxValue": tax_value,
                "Availability": availability,
                "FinalPrice": final_price,
                "LastUpdateTime": current_time_str
            }

            price_data.append(data_entry)

        return price_data
    
    # получение данных о картинках (gallery_images) из html
    # формат данных:
    # [{'Name': Название картинки, 'Value': Ссылка}, ...]
    def __get_images_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        image_elements = soup.find('div', class_='gallery__images')

        image_data = []
        image_data.append({ "Header": "ImagesData"})

        if image_elements == None or len(image_elements) == 0:
            single_img_element = soup.find('div', id="single_image_gallery_box")
            if single_img_element != None:
                image_url = single_img_element.a.img['src']
                if str(image_url).startswith("https:") == False:
                        image_url = "https:" + image_url

                url_parts = image_url.split('/')
                file_name = url_parts[-1]

                image_data.append({'Name': file_name, 'Value': image_url})
            else:
                return None
        else:
            li_elements = image_elements.find_all('li', class_='gallery__image')

            for image in li_elements:
                img_tag = image.find('img')
                if img_tag:
                    image_url = img_tag['src']
                    if str(image_url).startswith("https:") == False:
                        image_url = "https:" + image_url

                    url_parts = image_url.split('/')
                    file_name = url_parts[-1]
                    
                    image_data.append({'Name': file_name, 'Value': image_url})

        return image_data

    # полная очистка ресурсов web driver-а
    def __clear_web_driver(self):
        self.cloudlare_tor_driver.clear_web_drivers(self.web_driver)
        self.web_driver = None

    # получение данных с страницы комплектующих
    def get_data_from_page(self, link, part: Part):
        page_data = []
        while True:
            if self.web_driver == None:
                self.web_driver = self.cloudlare_tor_driver.get_driver(link)
            else:
                try:
                    self.web_driver.get(link)
                    if self.cloudlare_tor_driver.check_on_data_page(self.web_driver, link) == False:
                        self.logger.info(f"Link: {link}. Cloudflare страница.")
                        self.__clear_web_driver()
                        continue
                except TimeoutException:
                    self.logger.error(f"Link: {link}. TimeoutException ошибка обработана. get_data_from_page")
                    continue
                                            
            html = self.__get_html_from_products_page(link)

            if html == None or len(html) == 0:
                self.logger.info(f"Link: {link}. html равен None или 0.")
                self.__clear_web_driver()
                continue
            else:
                main_data, product_tag_main_data = self.__get_main_data(html, link, part)
                specification_data= self.__get_specification_table_data(html)

                if specification_data == None or len(specification_data) == 0:
                    self.logger.warning(f"Link: {link}. Specification data равен None или 0.")
                    self.__clear_web_driver()
                    continue
                
                product_tag = self.__get_product_tag(html)
                if product_tag == None:
                    self.logger.warning(f"Link: {link}. Страница не вернула product_tag.")
                    continue

                if product_tag != product_tag_main_data:
                    self.logger.info(f"Link: {link}. Страница вернула дупликат данных.")
                    continue

                user_rating_data = self.__get_user_ratings_table_data(html)
                prices_data = self.__get_prices_table_data(html)
                images_data = self.__get_images_data(html)

                page_data.append(main_data)
                page_data.append(specification_data)

                if user_rating_data == None or len(user_rating_data) == 0 or len(user_rating_data) == 1:
                    pass
                else:
                    page_data.append(user_rating_data)

                if prices_data == None or len(prices_data) == 0 or len(prices_data) == 1:
                    pass
                else:
                    page_data.append(prices_data)

                if images_data == None or len(images_data) == 0 or len(images_data) == 1:
                    pass
                else:
                    page_data.append(images_data)
                    
                return page_data

    # получение данных о комплектующих из json
    def get_pages_data_from_json(part: Part):
        current_directory = os.getcwd()
        file_path = current_directory + PARAMETERS_RELATIVE_PATH + str(part.value) + "_parameters.json"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                pages_data = json.load(json_file)
                json_file.close()
        except FileNotFoundError:
            return {}
            
        return pages_data
    
    # сохранение данных о комплектующих в json
    def save_pages_data_to_json(part: Part, data: dict):
        pages_data = Parameters.get_pages_data_from_json(part)

        if pages_data == {} or len(pages_data) == 0 or pages_data == None:
            existing_data = {}
        else:
            existing_data = pages_data

        existing_data.update(data)

        current_directory = os.getcwd()
        file_path = current_directory + PARAMETERS_RELATIVE_PATH + str(part.value) + "_parameters.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, indent=4, ensure_ascii=False)
            json_file.close()

    # получение данных о комплектующих конкретной категории
    def get_part_data(self, part: Part, start_index: int = 0):
        links = Links.get_links_from_json(part)

        part_data = {}
        for index in range(start_index, len(links)):
            page_data = self.get_data_from_page(links[index], part)
            part_data[str(index)] = page_data

            self.logger.info(f"{index}. Получены данные с страницы - Link: {links[index]}.")

            if index % 100 == 0:
                Parameters.save_pages_data_to_json(part, part_data)
                part_data = {}

        Parameters.save_pages_data_to_json(part, part_data)
        return part_data
    
    # метод получения последнего ключа из json файла с данными комплектующей
    def get_last_key_of_part(part: Part):
        part_data = Parameters.get_pages_data_from_json(part)
        
        if part_data == {}:
            last_key = 0
            return last_key
        
        last_key = list(part_data.keys())[-1]

        return int(last_key)
    
    # проверка на то запаршена ли комплектующая
    def is_all_parsed(part: Part):
        last_key = Parameters.get_last_key_of_part(part)
        links = Links.get_links_from_json(part)

        if int(last_key) + 1 == len(links):
            return True
        else:
            return False
        
    # получение всех данных
    def get_all_pages_data(self):
        for part in Part:
            if Parameters.is_all_parsed(part) == True:
                self.logger.info(f"Part: {part.value}. Все данные получены.")
                continue
            else:
                last_key = Parameters.get_last_key_of_part(part)

                self.logger.info(f"Part: {part.value}. LastKey: {last_key}.")

                if (last_key == 0):
                    start_index = 0
                else:
                    start_index = last_key + 1

                self.get_part_data(part, start_index)