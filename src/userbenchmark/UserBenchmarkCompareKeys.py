from .UserBenchmarkPart import UserBenchmarkPart
from .UserBenchmarkCompareKeyType import UserBenchmarkCompareKeyType
from .UserBenchmarkResources import UserBenchmarkResources

import json
import re

import os

# класс для получения compare keys
class UserBenchmarkCompareKeys:
    # метод возвращающий тип ссылки
    def get_link_type(self, link):
        if "SpeedTest" in link:
            return "SpeedTest"
        elif "Rating" in link:
            return "Rating"
        else:
            return "Unknown"
    
    # получение compare keys из ссылок
    def extract_compare_keys_from_links(self, links):
        keys = []
        compare_key_types = []
        i = 0

        for link in links:
            compare_key_type = UserBenchmarkCompareKeyType.WithoutM
            link_type = self.get_link_type(link)

            match = re.search(r'/(\d+)', link)

            i = i + 1
            key = None
            if match:
                key = match.group(1)
            else:
                key = None

            if link_type == "Rating":
                compare_key_type = UserBenchmarkCompareKeyType.WithoutM
            else:
                compare_key_type = UserBenchmarkCompareKeyType.WithM

            keys.append(key)
            compare_key_types.append(compare_key_type)

        return keys, compare_key_types

    # получение моделей
    def get_compare_keys_data(self, part: UserBenchmarkPart):
        links = UserBenchmarkResources.get_links_from_resources_csv(part)
        models = UserBenchmarkResources.get_models_from_resources_csv(part)

        keys, types = self.extract_compare_keys_from_links(links)

        return models, keys, types
    
    # получение compare ключей из json файла
    def get_compare_keys_from_json(part: UserBenchmarkPart):
        current_directory = os.getcwd()
        file_path = current_directory + "\\data\\userbenchmark\\compare_keys\\" + part.value + "_compare_keys.json"
        with open(file_path, 'r', encoding='utf-8') as json_file:
            compare_keys = json.load(json_file)
            
        return compare_keys

    # сохранение compare ключей в json
    def save_compare_keys_to_json(part: UserBenchmarkPart, data):
        current_directory = os.getcwd()
        save_directory = current_directory + "\\data\\userbenchmark\\compare_keys\\"
        filename = part.value + "_compare_keys"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    # получение compare ключей для всех типов комплектующих
    def get_all_compare_keys(self):
        for part in UserBenchmarkPart:
            models, keys, types = self.get_compare_keys_data(part)

            keys_data = {}
            for i in range(len(models)):
                keys_data[i] = { "model": models[i], "key": keys[i], "type": types[i].value }

            UserBenchmarkCompareKeys.save_compare_keys_to_json(part, keys_data)

if __name__ == "__main__":
    parser = UserBenchmarkCompareKeys()
    parser.get_all_compare_keys()