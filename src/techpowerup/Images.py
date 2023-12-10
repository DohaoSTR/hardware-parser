from .Part import Part
from ..RequestWebDriver import RequestWebDriver
from .Parameters import Parameters

import logging
from logging import Logger

import json
from urllib.parse import urlparse

import os

# получение изображений комплектующих с сайта Techpowerup
class Images:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        self.link = None

    # реакция при окончании работы или возникновение ошибки
    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info(f"Работа парсера завершена, Link: {self.link}")

        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")
        
        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    # метод для преобразования одной страницы данных в links element
    # возвращает PartKey комплектующей и ссылки для этой комплектующей
    def __get_image_section_data(page_data):
        part_key = next((item['Value'] for section in page_data for item in section[1:] if item.get("Name") == "PartKey"), None)
        links_element = next((section[1:] for section in page_data if section[0].get("Header") == "Links"), None)

        return part_key, links_element

    # метод получающий два списка:
    # keys - список содержащий PartKey для всех комплеткующих одной категории
    # links - список содержащий Link каждого изображения    
    # по сути keys[0] и links[0] - это данные одной изображения (ссылка на картинку и соответствующий ключ)
    def __get_image_links(part: Part):
        pages_data = Parameters.get_part_parameters_from_json(part)
        
        keys = []
        links = []

        for key, page_data in pages_data.items():
            part_key, links_element = Images.__get_image_section_data(page_data)

            keys.append(part_key)
            links.append(links_element)
        
        return keys, links
    
    # метод для сохранения кратких данных о изображениях, для конкретной категории комплектующих 
    # Формат данных
    # "Ссылка": {
    # "Name": "Название картинки",
    # "Keys": [Список с ключами комплеткующих, для которых данное изображение актуально]
    def __save_summary_part_data(part: Part):
        keys, links_elements = Images.__get_image_links(part)

        images_data = []

        for index, links_element in enumerate(links_elements):
            for link_element in links_element:
                name = link_element.get('Name', '')
                value = link_element.get('Value', '')
                images_data.append({ "Key": keys[index], "Name": name, "Value": value })

        new_data_dict = {}
        for item in images_data:
            value = item.get("Value")
            name = item.get("Name")
            key = item.get("Key")
                
            if value in new_data_dict:
                new_data_dict[value]["Keys"].append(key)
            else:
                new_data_dict[value] = {"Name": name, "Keys": [key]}

        current_file_path = os.path.abspath(__file__)
        save_directory = os.path.dirname(current_file_path) + "\\data\\images\\"
        filename = str(part.value) + "_images_links"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(new_data_dict, json_file, indent=4, ensure_ascii=False)

    #метод для сохранения кратких данных о изображениях, для всех категорий комплектующих
    def save_all_summary_parts_data(self):
        for part in Part:
            Images.__save_summary_part_data(part)

    # метод для получения кратких данных о изображениях, для категории комплектующих
    def __get_summary_part_data(part: Part):
        current_file_path = os.path.abspath(__file__)
        file_path = os.path.dirname(current_file_path) + "\\data\\images\\" + part.value + "_images_links.json"
        
        data = None
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        
        return data
    
    def __extract_paths_from_urls(self, link):
        parsed_url = urlparse(link)
        path = parsed_url.path
        if "/images/" in path:
                index = path.index("/images/") + len("/images/")
                path_after_images = path[index:]
                folder, filename = os.path.split(path_after_images)

        return folder, filename

    def __save_image(folder, filename, response):
        current_file_path = os.path.abspath(__file__)
        save_directory = os.path.dirname(current_file_path) + "\\data\\images\\" + folder + "\\"

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        with open(save_directory + filename, 'wb') as file:
            file.write(response.content)

    def save_part_images(self, part: Part):
        data = Images.__get_summary_part_data(part)

        index = 0
        for link, info in data.items():
            self.link = link

            folder, filename = self.__extract_paths_from_urls(link)
            request_web_driver = RequestWebDriver(self.logger)
            response = request_web_driver.get_response(link)

            Images.__save_image(folder, filename, response)

            self.logger.info(f"{index}. Картинка сохранена - Name: {filename}, Link: {link}")
            index = index + 1

    def save_all_images(self):
        for part in Part:
            self.save_part_images(part)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        encoding='utf-8')
    logger = logging.getLogger("techpowerup_images")
    file_handler = logging.FileHandler("techpowerup_parser\\logs\\techpowerup_images.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    parser = Images(logger)
    with parser:
        parser.save_all_summary_parts_data()
        parser.save_all_images()