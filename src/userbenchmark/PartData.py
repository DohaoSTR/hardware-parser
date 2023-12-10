from .CompareKeys import CompareKeys
from .UserBenchmarkRequest import UserBecnhmarkRequest
from .Part import Part
from .CompareKeyType import CompareKeyType

from ..misc import custom_float

import logging
from logging import Logger

import json
import re

from bs4 import BeautifulSoup

import os

EFFECTIVE_SPEED_TABLE_ID = 'effectivespeedtable'
AVERAGE_SCORE_TABLE_ID = 'primaryavgtable'
OVERCLOCKED_OR_PEAK_SCORE_TABLE_ID = 'primarytable'
VALUE_SENTIMENT_TABLE_ID = 'pricesenttable'
NICE_TO_HAVES_TABLE_ID = 'secondarytable'

# класс для парсинга данных комплектующих с сайта UserBenchmark
class PartData:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        web_driver = UserBecnhmarkRequest(logger)
        self.web_driver = web_driver

        self.link = None
        self.page_data = None

    # получение html content 
    def __get_html_content(self, link):
        self.link = link
        html_content = self.web_driver.get_html_content(link)

        return html_content
    
    def __split_value_and_unit(self, input_str):
        match_rub = re.match(r'^(?:руб|рубли)\s*([\d.,]+)$', input_str, re.IGNORECASE)
        if match_rub:
            value = match_rub.group(1).replace(",", ".")
            unit = "руб"
            return value, unit
        
        match_standard = re.match(r'([\d.,]+)\s*([^\d.,\s]+)', input_str)
        if match_standard:
            value = match_standard.group(1).replace(",", ".")
            unit = match_standard.group(2)
            return value, unit
        
        match_currency = re.match(r'^([€$£])(\d+)$', input_str)
        if match_currency:
            currency_symbol = match_currency.group(1)
            amount = int(match_currency.group(2))
            return amount, currency_symbol

        return None, None
    
    # получение standard table из html
    def __get_standard_table(self, html_content, table_id):
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('div', id = table_id)

        if table == None:
            self.logger.info(f"На странице нет {table_id}, Link: {self.link}")
            return None

        rows = table.find_all('tr')
        data = []

        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 7:
                text_parts  = columns[0].get_text().split('\\n')
                name = text_parts[0].strip()
                description = columns[0].find('span', class_ = 'comp-comparelabeldesc').text
                value_with_unit = columns[2].get_text(strip=True)

                value, unit_of_measure = self.__split_value_and_unit(value_with_unit)

                if value is not None:
                    data.append({ "Name": name, "Description": description, "Value": custom_float(value), "UnitOfMeasure": unit_of_measure })
                else:
                    data.append({ "Name": name, "Description": description, "Value": value, "UnitOfMeasure": unit_of_measure })

        return data
    
    # получение specification table из html
    def __get_specification_table(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('div', id='specstable')

        if table == None:
            self.logger.info(f"На странице нет specification_table, Link: {self.link}")
            return None
        
        rows = table.find_all('tr')
        data = []

        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 7:
                label = columns[0].get_text(strip=True)
                label = str(label).replace('\\n', ' ').replace('\\t', '').strip()
                value = columns[3].get_text(strip=True)
                data.append({ "Name": label, "Value": value})
        
        return data
    
    # метод для формирования compare ссылки
    def __form_compare_link(self, part: Part, key_type: CompareKeyType, key):
        link = None

        if key_type is CompareKeyType.WithM:
            link = "https://" + part.value + ".userbenchmark.com/Compare/vs-Group-/m" + key + "vs10"
        elif key_type is CompareKeyType.WithoutM:
            link = "https://" + part.value + ".userbenchmark.com/Compare/vs-Group-/" + key + "vs10"

        return link

    def get_part_data_from_json(part: Part):
        current_directory = os.getcwd()
        file_path = current_directory + "\\data\\userbenchmark\\part_data\\" + part.value + "_data.json"
        with open(file_path, 'r') as json_file:
            part_data = json.load(json_file)
            
        return part_data
      
    def save_part_data_to_json(part: Part, data):
        current_directory = os.getcwd()
        save_directory = current_directory + "\\data\\userbenchmark\\part_data\\"
        filename = part.value + "_data"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    # получение данных комплектующих для одной категории
    def get_part_data(self, compare_keys, part: Part):
        data = {}

        index = 0
        for key, value in compare_keys.items():
            compare_type_str = value['type']
            compare_key_type = None
            try:
                compare_key_type = CompareKeyType(compare_type_str)
            except ValueError:
                self.logger.info(f"Произошла ошибка при получении compare_key_type. Key - {key}")
                break

            compare_link = self.__form_compare_link(part, compare_key_type, value['key'])

            page_data = []
            html_content = self.__get_html_content(compare_link)
            if not isinstance(html_content, str):
                html_content = str(html_content)

            effective_speed_table_data = self.__get_standard_table(html_content, EFFECTIVE_SPEED_TABLE_ID)
            average_score_table_data = self.__get_standard_table(html_content, AVERAGE_SCORE_TABLE_ID)
            overclocked_or_peak_score_table_data = self.__get_standard_table(html_content, OVERCLOCKED_OR_PEAK_SCORE_TABLE_ID)
            value_sentiment_table_data = self.__get_standard_table(html_content, VALUE_SENTIMENT_TABLE_ID)
            nice_to_haves_table_data = self.__get_standard_table(html_content, NICE_TO_HAVES_TABLE_ID)
            specification_table_data = self.__get_specification_table(html_content)

            page_data = [{ "key": value['key'] }]
            if effective_speed_table_data is not None:
                page_data += effective_speed_table_data 
            if average_score_table_data is not None:
                page_data += average_score_table_data  
            if overclocked_or_peak_score_table_data is not None:
                page_data += overclocked_or_peak_score_table_data
            if value_sentiment_table_data is not None:
                page_data += value_sentiment_table_data
            if nice_to_haves_table_data is not None:
                page_data += nice_to_haves_table_data
            if specification_table_data is not None:
                page_data += specification_table_data

            self.page_data = page_data
            data[index] = page_data

            self.logger.info(f"{index}. Ссылка: {compare_link}")
            self.logger.info(f"key - {value['key']}")

            index = index + 1
            if index % 100 == 0:
                PartData.save_part_data_to_json(part, data)
        
        return data

    def get_all_parts_data(self):
        for part in Part:
            compare_keys = CompareKeys.get_compare_keys_from_json(part)

            data = self.get_part_data(compare_keys, part)
            PartData.save_part_data_to_json(part, data)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
    logger = logging.getLogger("userbenchmark_part_data_parser")
    file_handler = logging.FileHandler("userbenchmark_parser\\logs\\userbenchmark_part_data_parser.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    parser = PartData(logger)
    parser.get_all_parts_data()