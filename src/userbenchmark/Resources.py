from .Part import Part

from logging import Logger
import logging

import csv
import shutil

import os

import requests

# класс для скачивания resources в csv формате с сайта
class Resources:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")
        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    # получение ссылки на ресурс в зависмости от типа комплектующей
    def __get_resources_link(part: Part):
        return "https://www.userbenchmark.com/resources/download/csv/" + str(part.value).upper() + "_UserBenchmarks.csv"
    
    # метод для получения пути к файлу с csv ресурсами
    def __get_downloaded_file_path(part: Part):
        current_directory = os.getcwd()
        downloaded_file_path = current_directory + "\\data\\userbenchmark\\resources\\" + str(part.value).upper() + "_UserBenchmarks.csv"
        
        return downloaded_file_path
    
    # метод для проверки скачаны ли ресурсы
    def __is_resources_downloaded():
        for part in Part:
            downloaded_file_path = Resources.__get_downloaded_file_path(part)
                
            if os.path.isfile(downloaded_file_path):
                continue
            else:
                return False
            
        return True
    
    # метод для получения директории предназначенной для хранения ресурсов
    def __get_downloaded_file_directory():
        current_directory = os.getcwd()
        downloaded_file_directory = os.path.dirname(current_directory) + "\\data\\userbenchmark\\resources\\"

        return downloaded_file_directory
    
    # метод для удаления скачанных csv ресурсов с сайта
    def __delete_resources(self):
        downloaded_file_directory = Resources.__get_downloaded_file_directory()

        for item in os.listdir(downloaded_file_directory):
            item_path = os.path.join(downloaded_file_directory, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        self.logger.info(f"Очистка директории с csv ресурсами!")

    # метод для скачивания csv ресурса с сайта 
    def get_csv_resource(self, part: Part):
        if Resources.__is_resources_downloaded() == True:
            self.__delete_resources()
        
        while True:
            link = Resources.__get_resources_link(part)
            downloaded_file_path = Resources.__get_downloaded_file_path(part)

            response = requests.get(link)
            with open(downloaded_file_path, "wb") as file:
                file.write(response.content)

            if os.path.isfile(downloaded_file_path):
                break
            else:
                continue
        
        self.logger.info(f"{part.value} - csv ресурсы для данной категории комплектующих скачаны!")
    
    # метод для скачивания всех csv ресурсов с сайта
    def get_all_resources(self):
        for part in Part:
            self.get_csv_resource(part)

    # получение данных из csv ресурсов 
    def get_links_from_resources_csv(part: Part):
        current_directory = os.getcwd()
        csv_link = current_directory + "\\data\\userbenchmark\\resources\\" + part.value + "_UserBenchmarks.csv"

        with open(csv_link, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
                    
            column_number = 7
            column_values = []

            next(reader)

            for row in reader:
                if len(row) > column_number:
                    column_values.append(row[column_number])
                    
            return column_values
        
    def get_models_from_resources_csv(part: Part):
        current_directory = os.getcwd()
        csv_link = current_directory + "\\data\\userbenchmark\\resources\\" + part.value + "_UserBenchmarks.csv"

        with open(csv_link, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
                    
            column_number = 3
            column_values = []

            next(reader)

            for row in reader:
                if len(row) > column_number:
                    column_values.append(row[column_number])
                    
            return column_values

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
    logger = logging.getLogger("userbenchmark_fps_data_parser")
    file_handler = logging.FileHandler("userbenchmark_parser\\logs\\userbenchmark_fps_data_parser.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    parser = Resources(logger)
    with parser:
        parser.get_all_resources()