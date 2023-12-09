import csv
import json
import os
from typing import List

from src.userbenchmark.UserBenchmarkGameKeys import UserBenchmarkGameKeys
from src.userbenchmark.UserBenchmarkPart import UserBenchmarkPart
from src.userbenchmark.UserBenchmarkPartMetrics import UserBenchmarkPartMetrics
from src.userbenchmark.UserBenchmarkPartKeys import UserBenchmarkPartKeys
from src.userbenchmark.UserBenchmarkPartData import UserBenchmarkPartData
from src.userbenchmark.UserBenchmarkAsyncFPSData import UserBenchmarkAsyncFPSData

from src.userbenchmark.UserBenchmarkResolution import UserBenchmarkResolution
from src.userbenchmark.UserBenchmarkFPSCombination import UserBenchmarkFPSCombination
from src.userbenchmark.UserBenchmarkGameSettings import UserBenchmarkGameSettings
from src.userbenchmark.UserBenchmarkCompareKeyType import UserBenchmarkCompareKeyType

from src.userbenchmark.UserBenchmarkCompareKeys import UserBenchmarkCompareKeys
from src.userbenchmark.UserBenchmarkKeysHandling import UserBenchmarkKeysHandling

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

class UserBenchmarkAPI:
    #Type, PartNumber, Brand, Model, Rank, Benchmark, Samples, URL
    def get_resource(part: UserBenchmarkPart) -> List[PartEntity]:
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

        for part in UserBenchmarkPart:
            resource_data = UserBenchmarkAPI.get_resource(part)

            for item in resource_data:
                data.append(item)

        return data

    #
    def get_game_keys() -> dict:
        game_keys = UserBenchmarkGameKeys.get_game_keys_from_json()

        data = []
        for key, value in game_keys.items():
            data.append({ "Key": key, "Name": value })

        return data

    def get_game_keys_entities():
        game_keys = UserBenchmarkGameKeys.get_game_keys_from_json()

        data = []
        for key, value in game_keys.items():
            data.append(Game(key = key, name = value))

        return data
    #

    #
    def get_metrics_of_part(part: UserBenchmarkPart):
        metrics_data = UserBenchmarkPartMetrics.get_metric_values_from_json(part)

        data = []
        for index, value in metrics_data.items():
            data.append({ "Key": int(value["key"]), 
                          "Gaming": value["gaming_percentage"], 
                          "Desktop": value["desktop_percentage"], 
                          "Workstation": value["workstation_percentage"]  })

        return data

    def get_metrics_of_all_parts():
        data = []

        for part in UserBenchmarkPart:
            metrics_data = UserBenchmarkAPI.get_metrics_of_part(part)

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
        class_names_mapping = UserBenchmarkAPI.__get_part_mapping("class_names")
        for key, value in class_names_mapping.items():
            if key == class_name:
                return value
            
    def get_data_of_part(part: UserBenchmarkPart):
        part_data = UserBenchmarkPartData.get_part_data_from_json(part)
        mapping = UserBenchmarkAPI.__get_part_mapping(part.value)

        metrics_class_name = UserBenchmarkAPI.__get_entity_class_name(part.value)
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
    def get_parameters_summary_data_of_part(part: UserBenchmarkPart):
        part_data = UserBenchmarkPartData.get_part_data_from_json(part)

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

    def save_parameters_summary_data_of_part_to_json(summary_data, part: UserBenchmarkPart):
        current_directory = os.getcwd()
        file_path = current_directory + SUMMARY_DATA_RELATIVE_PATH + str(part.value) + "_unique_names.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(summary_data, json_file, indent=4, ensure_ascii=False)

    def save_all_parameters_summary_data_to_json():
        for part in UserBenchmarkPart:
            summary_data = UserBenchmarkAPI.get_parameters_summary_data_of_part(part)
            UserBenchmarkAPI.save_parameters_summary_data_of_part_to_json(summary_data, part)
    #



    #
    def get_keys_of_part(part: UserBenchmarkPart):
        part_keys = UserBenchmarkPartKeys.get_part_keys_from_json(part)
        data = []

        for index, value in part_keys.items():
            data.append({ "Key": int(value["key"]), 
                          "Model": value["model"] })

        return data

    def get_keys_of_all_parts():
        data = []

        for part in UserBenchmarkPart:
            part_keys = UserBenchmarkAPI.get_keys_of_part(part)

            for item in part_keys:
                data.append(item)

        return data

    def get_compare_keys_of_part(part: UserBenchmarkPart):
        compare_keys = UserBenchmarkCompareKeys.get_compare_keys_from_json(part)
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

        for part in UserBenchmarkPart:
            compare_keys = UserBenchmarkAPI.get_compare_keys_of_part(part)

            for item in compare_keys:
                data.append(item)

        return data
    #



    #
    def get_handled_keys_of_part(part: UserBenchmarkPart):
        handled_keys = UserBenchmarkKeysHandling.get_handled_part_keys_from_json(part)

        data = []

        for index, value in handled_keys.items():
            data.append({ "Key": int(value["key"]), 
                          "Model": value["model"] })

        return data

    def get_handled_keys_of_all_parts():
        data = []

        for part in UserBenchmarkPart:
            handled_keys = UserBenchmarkAPI.get_handled_keys_of_part(part)

            for item in handled_keys:
                data.append(item)

        return data

    def get_keys_without_duplicates_of_part(part: UserBenchmarkPart):
        part_keys = UserBenchmarkKeysHandling.get_part_keys_without_duplicates_from_json(part)

        data = []

        for index, value in part_keys.items():
            data.append({ "Key": int(value["key"]), 
                          "Model": value["model"] })

        return data
    
    def get_keys_without_duplicates_of_all_parts():
        data = []

        for part in UserBenchmarkPart:
            part_keys = UserBenchmarkAPI.get_keys_without_duplicates_of_part(part)

            for item in part_keys:
                data.append(item)

        return data
    #

    #
    def get_fps_data():
        pass

    def get_all_fps_data():
        pass