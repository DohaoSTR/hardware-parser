import csv
from enum import Enum
import json
import os
from typing import List

from src.userbenchmark.GameKeys import GameKeys
from src.userbenchmark.Part import Part
from src.userbenchmark.PartMetrics import PartMetrics
from src.userbenchmark.PartKeys import PartKeys
from src.userbenchmark.PartData import PartData
from src.userbenchmark.AsyncFPSData import AsyncFPSData

from src.userbenchmark.Resolution import Resolution
from src.userbenchmark.FPSCombination import FPSCombination
from src.userbenchmark.GameSettings import GameSettings

from src.userbenchmark.CompareKeys import CompareKeys
from src.userbenchmark.KeysHandling import KeysHandling

from .local_entities.CPU import CPU
from .local_entities.GPU import GPU
from .local_entities.HDD import HDD
from .local_entities.SSD import SSD
from .local_entities.RAM import RAM

from .db_entities.PartEntity import PartEntity
from .db_entities.Game import Game
from .db_entities.Metric import Metric

SUMMARY_DATA_RELATIVE_PATH = "\\data\\userbenchmark\\summary_data\\"
PARAMETERS_MAPPING_RELATIVE_PATH = "\\data\\userbenchmark\\parameters_mapping\\"

class API:
    def get_resource(part: Part) -> List[PartEntity]:
        current_directory = os.getcwd()
        csv_link = current_directory + "\\data\\userbenchmark\\resources\\" + part.value + "_UserBenchmarks.csv"

        data = []
        with open(csv_link, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            next(reader)
            
            for row in reader:    
                type = row[0]
                part_number = row[1]
                brand = row[2]
                model = row[3]
                rank = row[4]
                benchmark = row[5]
                samples = row[6]
                url = row[7]

                if url == "":
                    url = None

                if type == "":
                    type = None

                if part_number == "":
                    part_number = None

                if brand == "":
                    brand = None

                if model == "":
                    model = None

                data.append(PartEntity( 
                    type = type,
                    part_number = part_number,
                    brand = brand,
                    model = model,
                    rank = int(rank),
                    benchmark = float(benchmark),
                    samples = int(samples),
                    url = url))
        
        return data

    def get_resources() -> List[PartEntity]:
        data = []

        for part in Part:
            resource_data = API.get_resource(part)

            for item in resource_data:
                data.append(item)

        return data

    #
    def get_game_keys() -> dict:
        game_keys = GameKeys.get_game_keys_from_json()

        data = []
        for key, value in game_keys.items():
            data.append({ "Key": key, "Name": value })

        return data

    def get_game_keys_entities():
        game_keys = GameKeys.get_game_keys_from_json()

        data = []
        for key, value in game_keys.items():
            data.append(Game(key = key, name = value))

        return data
    #

    #
    def get_metrics_of_part(part: Part):
        metrics_data = PartMetrics.get_metric_values_from_json(part)

        data = []
        for index, value in metrics_data.items():
            data.append({ "Key": int(value["key"]), 
                          "Gaming": value["gaming_percentage"], 
                          "Desktop": value["desktop_percentage"], 
                          "Workstation": value["workstation_percentage"]  })

        return data

    def get_metrics_of_all_parts():
        data = []

        for part in Part:
            metrics_data = API.get_metrics_of_part(part)

            for item in metrics_data:
                data.append(item)

        return data
    #

    #
    def __get_part_mapping(mapping_name: str):
        current_directory = os.getcwd()
        file_path = current_directory + PARAMETERS_MAPPING_RELATIVE_PATH + mapping_name + "_mapping.json"

        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                pages_data = json.load(json_file)
                json_file.close()
        except FileNotFoundError:
            return {}
            
        return pages_data
    
    def __get_entity_class_name(class_name: str):
        class_names_mapping = API.__get_part_mapping("class_names")
        for key, value in class_names_mapping.items():
            if key == class_name:
                return value
            
    def get_data_of_part(part: Part):
        part_data = PartData.get_part_data_from_json(part)
        mapping = API.__get_part_mapping(part.value)

        metrics_class_name = API.__get_entity_class_name(part.value)
        class_instance = globals()[metrics_class_name]

        data = []

        for index, item_block in part_data.items():
            part_key = None
            parameters = {}
            for parameter_blocks in item_block:
                if len(parameter_blocks) == 1:
                    part_key = parameter_blocks["key"]
                elif len(parameter_blocks) == 2:
                    name = parameter_blocks["Name"]
                    value = parameter_blocks["Value"]

                    mapping_name = mapping[name]
                    parameters[mapping_name] = value
                else:
                    name = parameter_blocks["Description"]
                    value = parameter_blocks["Value"]

                    mapping_name = mapping[name]
                    parameters[mapping_name] = value
            
            parameters["key"] = part_key

            entity = class_instance(**parameters)
            data.append(entity)

        return data
    #



    #
    def get_parameters_summary_data_of_part(part: Part):
        part_data = PartData.get_part_data_from_json(part)

        parameters_summary_data = {}
        for index, item_block in part_data.items():
            for parameter_blocks in item_block:
                if len(parameter_blocks) > 1:
                    if len(parameter_blocks) == 2:
                        name = parameter_blocks["Name"]
                    else:
                        name = parameter_blocks["Description"]
                    value = parameter_blocks["Value"]

                    if name not in parameters_summary_data:
                        parameters_summary_data[name] = {"types": {}, "count": 0, "max_value": None, "unique_values": [], "unique_values_count": 0 }
                    
                    value_type = type(value).__name__

                    if value_type not in parameters_summary_data[name]["types"]:
                        parameters_summary_data[name]["types"][value_type] = 0
                    parameters_summary_data[name]["types"][value_type] += 1

                    parameters_summary_data[name]["count"] += 1

                    if (isinstance(value, (int, float)) and (parameters_summary_data[name]["max_value"] is None or value > parameters_summary_data[name]["max_value"])) and isinstance(parameters_summary_data[name]["max_value"], list) == False:
                        parameters_summary_data[name]["max_value"] = value
                    elif (isinstance(value, str) and (parameters_summary_data[name]["max_value"] is None or len(value) > len(parameters_summary_data[name]["max_value"]))) and isinstance(parameters_summary_data[name]["max_value"], list) == False:
                        parameters_summary_data[name]["max_value"] = value
                    elif isinstance(value, list) and (parameters_summary_data[name]["max_value"] is None or len(value) > len(parameters_summary_data[name]["max_value"])):
                        parameters_summary_data[name]["max_value"] = value

                    if value not in parameters_summary_data[name]["unique_values"]:
                        if len(parameters_summary_data[name]["unique_values"]) > 25:
                            pass
                        else:
                            parameters_summary_data[name]["unique_values"].append(value)
                        parameters_summary_data[name]["unique_values_count"] += 1

        return parameters_summary_data

    def save_parameters_summary_data_of_part_to_json(summary_data, part: Part):
        current_directory = os.getcwd()
        file_path = current_directory + SUMMARY_DATA_RELATIVE_PATH + str(part.value) + "_unique_names.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(summary_data, json_file, indent=4, ensure_ascii=False)

    def save_all_parameters_summary_data_to_json():
        for part in Part:
            summary_data = API.get_parameters_summary_data_of_part(part)
            API.save_parameters_summary_data_of_part_to_json(summary_data, part)
    #



    #
    def get_keys_of_part(part: Part):
        part_keys = PartKeys.get_part_keys_from_json(part)
        data = []

        for index, value in part_keys.items():
            data.append({ "Key": int(value["key"]), 
                          "Model": value["model"] })

        return data

    def get_keys_of_all_parts():
        data = []

        for part in Part:
            part_keys = API.get_keys_of_part(part)

            for item in part_keys:
                data.append(item)

        return data

    def get_compare_keys_of_part(part: Part):
        compare_keys = CompareKeys.get_compare_keys_from_json(part)
        data = []

        for index, value in compare_keys.items():
            type = value["type"]

            if type == "":
                type = "without m"

            data.append({ "Key": int(value["key"]), 
                          "Model": value["model"],
                          "Type": type })

        return data

    def get_compare_keys_of_all_parts():
        data = []

        for part in Part:
            compare_keys = API.get_compare_keys_of_part(part)

            for item in compare_keys:
                data.append(item)

        return data
    #



    #
    def get_handled_keys_of_part(part: Part):
        handled_keys = KeysHandling.get_handled_part_keys_from_json(part)

        data = []

        for index, value in handled_keys.items():
            data.append({ "Key": int(value["key"]), 
                          "Model": value["model"] })

        return data

    def get_handled_keys_of_all_parts():
        data = []

        for part in Part:
            handled_keys = API.get_handled_keys_of_part(part)

            for item in handled_keys:
                data.append(item)

        return data

    def get_keys_without_duplicates_of_part(part: Part):
        part_keys = KeysHandling.get_part_keys_without_duplicates_from_json(part)

        data = []

        for index, value in part_keys.items():
            data.append({ "Key": int(value["key"]), 
                          "Model": value["model"] })

        return data
    
    def get_keys_without_duplicates_of_all_parts():
        data = []

        for part in Part:
            part_keys = API.get_keys_without_duplicates_of_part(part)

            for item in part_keys:
                data.append(item)

        return data
    #

    #
    def __get_fps_in_game_data(json_data, 
                               fps_combination: FPSCombination, 
                               resolution: Resolution,
                               game_settings: GameSettings,
                               game_key, 
                               index):
        data = {}
        for key, values in json_data.items():
            fps_value = 0
            samples_value = 0
            cpu_key = 0
            gpu_key = 0
            for field, value in values.items():
                if field == "fps_value":
                    fps_value = value
                elif field == "samples_value":
                    samples_value = value

            if fps_combination is FPSCombination.CPU:
                cpu_key = values["cpu_key"]
                gpu_key = 0
            elif fps_combination is FPSCombination.GPU:
                cpu_key = 0
                gpu_key = values["gpu_key"]
            elif fps_combination is FPSCombination.GPU_CPU:
                gpu_key = values["gpu_key"]
                cpu_key = values["cpu_key"]

            game_settings_value = GameSettings.get_database_value(game_settings.value)
            resolution_value = Resolution.get_database_value(resolution.value)

            data[index] = {
                "cpu_key": int(cpu_key),
                "gpu_key": int(gpu_key),
                "fps_value": fps_value,
                "samples_value": samples_value,
                "game_key": int(game_key),
                "game_settings": game_settings_value,
                "resolution": resolution_value }
                            
            index = index + 1

        return data, index

    def parse_fps_folder_name(name_folder: str):
        elements = name_folder.split("_")

        combination = None
        resolution = None
        game_settings = None
        if len(elements) == 4:
            combination = FPSCombination.GPU_CPU
            game_settings = GameSettings.get_part_enum(elements[2])
            resolution = Resolution.get_part_enum(elements[3])
        elif len(elements) == 3:
            combination = FPSCombination.get_part_enum(elements[0])
            game_settings = GameSettings.get_part_enum(elements[1])
            resolution = Resolution.get_part_enum(elements[2])

        return { 
            "Combination": combination,
            "Resolution": resolution,
            "GameSettings": game_settings
        }

    def get_fps_in_games_folder(name_folder: str):
        current_directory = os.getcwd()
        folder_path = current_directory + "\\data\\userbenchmark\\fps_in_games\\" + name_folder + "\\"

        settings_item = API.parse_fps_folder_name(name_folder)

        data = {}
        index = 0

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as json_file:
                    try:
                        json_data = json.load(json_file)

                        game_key = None
                        if settings_item["Combination"] == FPSCombination.GPU_CPU:
                            game_key = str(filename.split("_")[2])
                        else:
                            game_key = str(filename.split("_")[1])

                        dict, index = API.__get_fps_in_game_data(json_data, 
                                                                 settings_item["Combination"], 
                                                                 settings_item["Resolution"],
                                                                 settings_item["GameSettings"],
                                                                 game_key, 
                                                                 index)
                        data.update(dict)
                    except json.JSONDecodeError as e:
                        print(f"Ошибка при чтении файла {file_path}: {e}")

        return data

    def get_all_fps_data():
        all_fps_data = []
        
        current_directory = os.getcwd()
        folder_path = current_directory + "\\data\\userbenchmark\\fps_in_games\\"

        for name_folder in os.listdir(folder_path):
            data = API.get_fps_in_games_folder(name_folder)
            values_list = list(data.values())
            all_fps_data = all_fps_data + values_list
        
        return all_fps_data