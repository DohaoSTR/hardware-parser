from .UserBenchmarkPart import UserBenchmarkPart
from .UserBenchmarkResources import UserBenchmarkResources
from .UserBenchmarkRequest import UserBecnhmarkRequest

from logging import Logger
import logging

import json
import re

from bs4 import BeautifulSoup

import os

# класс для получения ключей для каждой комплектующей
# данные ключи необходимы для работы с вкладками FPS и BUILD
class UserBenchmarkPartKeys:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)
    
        web_driver = UserBecnhmarkRequest(logger)
        self.web_driver = web_driver
    
    # берет key для тех комплектующих которые имеют /Rating/ в запросе, такие
    # комплектующие содержат изначально неверный key
    def __get_key_from_link(self, key):
        compare_link = "https://gpu.userbenchmark.com/Compare/vs-Group-/" + key + "vs10"
        self.link = compare_link

        try:
            html_content = self.web_driver.get_html_content(compare_link)

            soup = BeautifulSoup(html_content, 'html.parser')
        
            link_elements = soup.find_all('a', class_='blacktext boxthumb btn-block')    
            for link_element in link_elements:
                link = link_element['href']

                if "/PCBuilder/Custom/" in link:
                    match = re.search(r'S0-M(\d+)', link)
                    if match:
                        number = match.group(1)
                        return number
                    else:
                        return None
        except Exception as e:
            self.logger.info(f"Произошла обшика: {str(e)}.")
            return None
    
    # получение ключей для работы с вкладкой FPS и BUILD
    def __extract_keys_from_links(self, links):
        keys = []
        index = 0

        for link in links:
            match = re.search(r'/(\d+)', link)

            index = index + 1

            key = None
            if match:
                key = match.group(1)

            if '/Rating/' in link:
                key = self.__get_key_from_link(key)   

            self.logger.info(f"№.{index}, key - {key}")

            keys.append(key)

        return keys
    
    # получение ключей + модели
    def __get_keys_data(self, part: UserBenchmarkPart):
        links = UserBenchmarkResources.get_links_from_resources_csv(part)
        models = UserBenchmarkResources.get_models_from_resources_csv(part)

        keys = self.__extract_keys_from_links(links)

        return models, keys

    # метод для получения ключей из json файла
    def get_part_keys_from_json(part: UserBenchmarkPart):
        current_directory = os.getcwd()
        file_path = current_directory + "\\data\\userbenchmark\\part_keys\\" + part.value + "_keys.json"
        with open(file_path, 'r', encoding='utf-8') as json_file:
            part_keys = json.load(json_file)
            
        return part_keys
    
    # метод для сохраненяи ключей в json файл
    def save_part_keys_to_json(part: UserBenchmarkPart, data):
        current_directory = os.getcwd()
        save_directory = current_directory + "\\data\\userbenchmark\\part_keys\\"
        filename = part.value + "_keys"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
    
    # метод получения ключей для всех комплектующих
    def get_all_part_keys(self):
        for part in UserBenchmarkPart:
            models, keys = self.__get_keys_data(part)

            keys_data = {}
            for i in range(len(models)):
                keys_data[i] = { "model": models[i], "key": keys[i] }

            UserBenchmarkPartKeys.save_part_keys_to_json(part, keys_data)