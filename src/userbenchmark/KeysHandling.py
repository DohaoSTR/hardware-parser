from .Part import Part

import json
import os

# класс для взаимодействия c ключами комплектующих
class KeysHandling():
    def get_handled_part_keys_from_json(part: Part):
        current_directory = os.getcwd()
        file_path = current_directory + "\\data\\userbenchmark\\handled_part_keys\\" + part.value + "_keys.json"

        with open(file_path, 'r', encoding='utf-8') as json_file:
            part_keys = json.load(json_file)
            
        return part_keys

    def save_handled_fps_keys_to_json(part: Part, data):
        current_directory = os.getcwd()
        save_directory = current_directory + "\\data\\userbenchmark\\handled_part_keys\\"
        filename = part.value + "_keys"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def get_part_keys_without_duplicates_from_json(part: Part):
        current_directory = os.getcwd()
        file_path = current_directory + "\\data\\userbenchmark\\part_keys_without_duplicates\\" + part.value + "_keys.json"

        with open(file_path, 'r', encoding='utf-8') as json_file:
            part_keys = json.load(json_file)
            
        return part_keys
    
    def save_part_keys_without_duplicates_to_json(part: Part, data):
        current_directory = os.getcwd()
        save_directory = current_directory + "\\data\\userbenchmark\\part_keys_without_duplicates\\"
        filename = part.value + "_keys"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)