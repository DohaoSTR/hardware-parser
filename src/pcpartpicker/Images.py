from .Parameters import Parameters
from .Part import Part

from ..RequestWebDriver import RequestWebDriver

from logging import Logger
import logging

import json
import os

IMAGES_RELATIVE_PATH = "\\data\\pcpartpicker\\images\\"
SUMMARY_IMAGES_DATA_RELATIVE_PATH = "\\data\\pcpartpicker\\images\\links\\"

# класс для получения изображений комплектующих
# и работы с изображениями
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

    # получение краткой информации о ссылках на изображения
    def get_summary_part_images(part_data):
        results = []
        for item_id, item_data in part_data.items():
            name = item_data[0][1]['Name']
            part_type = item_data[0][2]['PartType']
            link = item_data[0][3]['Link']
            key = item_data[0][4]['Key']
            
            images_section = None
            for section in item_data:
                if section[0]['Header'] == 'ImagesData':
                    images_section = section
                    break
            if images_section:
                images = images_section[1:]
                for image in images:
                    image_name = image.get('Name')
                    image_url = image.get('Value')
                    
                    if image_name != None and image_url != None:
                        result = {
                            'Name': name,
                            'PartType': part_type,
                            'Link': link,
                            'Key': key,
                            'ImageName': image_name, 
                            'ImageUrl': image_url
                        }
                        
                        results.append(result)

        return results
    
    # сохранение краткой информации о ссылках на изображения
    def save_summary_part_images_to_json(part_data, part: Part):
        current_file_path = os.path.abspath(__file__)
        save_directory = os.path.dirname(current_file_path) + "\\data\\images\\links\\"
        filename = part.value[0] + "_summary"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(part_data, json_file, indent=4, ensure_ascii=False)

    # сохранение краткой информации об всех ссылках на изображения
    def save_all_summary_part_images():
        for part in Part:
            part_data = Parameters.get_pages_data_from_json(part)
            summary_part_images = Images.get_summary_part_images(part_data)
            Images.save_summary_part_images_to_json(summary_part_images, part)

    # получение данных о каждом изображении в формате:
    # { Filename: имя файла для сохранения, Link: ссылка}
    def get_image_items(part_data):
        image_urls = set()
        image_items = []

        for cpu in part_data.values():
            for section in cpu:
                if section[0]['Header'] == 'ImagesData':
                    for item in section[1:]:
                        if item['Name'].endswith('.jpg'):
                            url = item['Value']

                            if url not in image_urls:
                                image_urls.add(url)

                                image_items.append({
                                    'Filename': item['Name'],
                                    'Link': item['Value']
                                })

        return image_items
    
    # сохранение одного изображения
    def __save_image(filename, response):
        current_directory = os.getcwd()
        save_directory = current_directory + IMAGES_RELATIVE_PATH

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        with open(save_directory + filename, 'wb') as file:
            file.write(response.content)

    # сохранение всех изображений одной категории комплектующих
    def save_images(self, image_items):
        index = 0
        for image_item in image_items:
            filename = image_item['Filename']
            link = image_item['Link']

            request_web_driver = RequestWebDriver(self.logger)
            response = request_web_driver.get_response(link)
            Images.__save_image(filename, response)

            self.logger.info(f"{index}. Получено изображение - Link: {link}.")
            index = index + 1

    # сохранения всех изображений для каждой комплектующей
    def save_images_for_all_parts(self):
        for part in Part:
            part_data = Parameters.get_pages_data_from_json(part)
            image_items = Images.get_image_items(part_data)
            self.save_images(image_items)
    
    def get_image_from_file(filename: str):
        current_directory = os.getcwd()
        file_path = current_directory + IMAGES_RELATIVE_PATH + filename

        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()

        return image_bytes

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
    logger = logging.getLogger("pcpartpicker_images")
    file_handler = logging.FileHandler("pcpartpicker_parser\\logs\\pcpartpicker_images.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    parser = Images(logger)
    with parser:
        Images.save_all_summary_part_images()
        parser.save_images_for_all_parts()