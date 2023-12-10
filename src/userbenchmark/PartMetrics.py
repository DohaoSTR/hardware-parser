from .UserBenchmarkRequest import UserBecnhmarkRequest
from .Part import Part
from .PartKeys import PartKeys
from .Resources import Resources

import logging
from logging import Logger

import json
import re

from bs4 import BeautifulSoup

import os

# класс для получения метрик с сайта UserBenchmark
class PartMetrics:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        
        web_driver = UserBecnhmarkRequest(logger)
        self.web_driver = web_driver

        self.link = None
        self.metric_value = None
        self.metric_name = None

    # получение метрик с страницы (3 div)
    def __get_metrics_from_page(self, link):
        self.link = link

        try:
            html_content = self.web_driver.get_html_content(link)
            soup = BeautifulSoup(html_content, 'html.parser')

            percentage_divs = soup.find_all('div', class_='bsc-w text-left semi-strong')
            list = []
            for div in percentage_divs:
                percentage_text = div.find('div').text
                list.append(percentage_text)

            return list[0], list[1], list[2]
        except Exception as e:
            self.logger.info(f"Произошла обшика: {str(e)}.")
            return None, None, None
    
    # конвертируем полученный div.text в значения
    def __convert_metric_string_to_values(self, metric_string):
        match = re.match(r'(\w+) (\d+)%', metric_string)

        gaming_text = None
        percentage_value = None
        if match:
            gaming_text = match.group(1)
            percentage_value = int(match.group(2))
        else:
            self.logger.info(f"Совпадение не найдено в полученном percentage_text.")
        
        return gaming_text, percentage_value
    
    # сохранение метрик
    def save_metric_names_to_json(part: Part, data):
        current_directory = os.getcwd()
        save_directory = current_directory + "\\data\\userbenchmark\\metrics\\"
        filename = part.value + "_metric_names"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def save_metric_values_to_json(part: Part, data):
        current_directory = os.getcwd()
        save_directory = current_directory + "\\data\\userbenchmark\\metrics\\"
        filename = part.value + "_metric_values"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    # получение метрик
    def get_metric_names_from_json(part: Part):
        current_directory = os.getcwd()
        file_path = current_directory + "\\data\\userbenchmark\\metrics\\" + part.value + "_metric_names.json"
        with open(file_path, 'r') as json_file:
            metric_names = json.load(json_file)
            
        return metric_names
    
    def get_metric_values_from_json(part: Part):
        current_directory = os.getcwd()
        file_path = current_directory + "\\data\\userbenchmark\\metrics\\" + part.value + "_metric_values.json"
        with open(file_path, 'r') as json_file:
            metric_values = json.load(json_file)
            
        return metric_values
    
    # получаем метрики для конкретного типа комплектующих
    def __get_part_metrics(self, links, part_keys, part: Part):
        metric_values = {}
        metric_names = {}

        index = 0
        for link in links:
            gaming_string, desktop_string, workstation_string = self.__get_metrics_from_page(link)

            self.logger.info(f"{index}. Ссылка: {link} ")
            if gaming_string or desktop_string or workstation_string != None:
                gaming_name, gaming_percentage = self.__convert_metric_string_to_values(gaming_string)
                desktop_name, desktop_percentage = self.__convert_metric_string_to_values(desktop_string)
                workstation_name, workstation_percentage = self.__convert_metric_string_to_values(workstation_string)

                self.metric_value = { "key": part_keys[index], "gaming_percentage": gaming_percentage, 
                                     "desktop_percentage": desktop_percentage, "workstation_percentage": workstation_percentage }
                self.metric_name = { "key": part_keys[index], "gaming_name": gaming_name, 
                                    "desktop_name": desktop_name, "workstation_name": workstation_name }

                metric_values[index] = { "key": part_keys[index], "gaming_percentage": gaming_percentage, 
                                        "desktop_percentage": desktop_percentage, "workstation_percentage": workstation_percentage }
                metric_names[index] = { "key": part_keys[index], "gaming_name": gaming_name, 
                                       "desktop_name": desktop_name, "workstation_name": workstation_name }  
                
                self.logger.info(f"metric_values - {self.metric_value}")
                self.logger.info(f"metric_name - {self.metric_name}")
            else:
                self.logger.info(f"В одном из значений вернулось - None. Gaming - {gaming_string}, Desktop - {desktop_string}, Workstation - {workstation_string}")

            index = index + 1
            if index % 100 == 0:
                PartMetrics.save_metric_names_to_json(part, metric_names)
                PartMetrics.save_metric_values_to_json(part, metric_values)

        return metric_names, metric_values
    
    # получение метрик для всех комплектующих
    def get_all_metrics(self):
        for part in Part:
            part_keys = PartKeys.get_part_keys_from_json(part)

            # преобразуем dict "index": { "model": "value", "key": "value"}
            # в list "key": "value"
            key_values = []
            for key, value in part_keys.items():
                if 'key' in value:
                    key_values.append(value['key'])

            links = Resources.get_links_from_resources_csv(part)

            metric_names, metric_values = self.__get_part_metrics(links, key_values, part)
            
            PartMetrics.save_metric_names_to_json(part, metric_names)
            PartMetrics.save_metric_values_to_json(part, metric_values)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
    logger = logging.getLogger("userbenchmark_part_metrics")
    file_handler = logging.FileHandler("userbenchmark_parser\\logs\\userbenchmark_part_metrics.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    parser = PartMetrics(logger)
    parser.get_all_metrics()