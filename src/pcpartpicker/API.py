from .Parameters import Parameters
from .Part import Part
from .Links import Links
from .Images import Images

from .db_entities.PartEntity import PartEntity

from .local_entities.CPUEntity import CPUEntity
from .local_entities.GPUEntity import GPUEntity
from .local_entities.CaseEntity import CaseEntity
from .local_entities.CaseFanEntity import CaseFanEntity
from .local_entities.CPUCoolerEntity import CPUCoolerEntity
from .local_entities.InternalHardDriveEntity import InternalHardDriveEntity
from .local_entities.MemoryEntity import MemoryEntity
from .local_entities.MotherboardEntity import MotherboardEntity
from .local_entities.PowerSupplyEntity import PowerSupplyEntity

import json
import os

from typing import List

PARAMETERS_MAPPING_RELATIVE_PATH = "\\data\\pcpartpicker\\parameters_mapping\\"
UNIQUE_SPECIFICATION_NAMES_RELATIVE_PATH = "\\data\\pcpartpicker\\unique_specification_names\\"

class API:
    # метод для получения данных о конкретной категории
    def get_data_of_part(part: Part) -> dict:
        pages_data = Parameters.get_pages_data_from_json(part)

        return pages_data
    
    # метод для получения всех данных
    def get_data_of_all_parts() -> dict:
        data = {}
        
        index = 0
        for part in Part:
            part_data = API.get_data_of_part(part)
            for key, value in part_data.items():
                data[index] = value
                index = index + 1

        return data
    #!
    #!
    #!



    #!
    #!
    #!
    # получить основные данные для таблицы pcpartpicker_part
    def get_part_entities_of_part(part: Part) -> List[PartEntity]:
        part_data = API.get_data_of_part(part)

        mapping = API.__get_part_mapping("part_entity")
        class_name = API.__get_local_entity_class_name("part")
        my_instance = globals()[class_name]

        entities = []
        for block_key, block_data in part_data.items():
            parameters = {}
            key = None

            for item in block_data:
                if any(entry.get("Header") == "Main" for entry in item):
                    parameters["name"] = item[1]["Name"]
                    parameters["part_type"] = item[2]["PartType"]
                    parameters["link"] = item[3]["Link"]
                    parameters["key"] = item[4]["Key"]
                
                if any(entry.get("Header") == "SpecificationTable" for entry in item):
                    for entry in item:
                        if "Name" in entry and "Value" in entry:
                            for key, value in mapping.items():
                                if value == entry["Name"]:
                                    parameters[key] = entry["Value"]

            entity = my_instance(**parameters)
            entities.append(entity)
        
        return entities
    
    # получить основные данные для таблицы pcpartpicker_part для всех категорий
    def get_part_entities_of_all_parts() -> List[PartEntity]:
        parts_entities = []
        
        for part_enum_item in Part:
            part_entity = API.get_part_entities_of_part(part_enum_item)
            parts_entities += part_entity
        
        return parts_entities
    #!
    #!
    #!



    #!
    #!
    #!
    # получить данные о part# для для таблицы pcpartpicker_part_number 
    def get_part_number_data(part: Part):
        part_data = API.get_data_of_part(part)

        data = []
        for block_key, block_data in part_data.items():
            key = None
            part_number = None

            for item in block_data:
                if any(entry.get("Header") == "Main" for entry in item):
                    key = item[4]["Key"]
                
                if any(entry.get("Header") == "SpecificationTable" for entry in item):
                    for entry in item:
                        if "Name" in entry and "Value" in entry:
                            if entry["Name"] == "Part #":
                                part_number = entry["Value"]
            
            if isinstance(part_number, list):
                for item in part_number:
                    data.append([ key, item ])
            else:
                data.append([ key, part_number ])
        
        return data
    
    # получить данные о part# для для таблицы pcpartpicker_part_number для всех категорий
    def get_part_number_data_of_all_parts():
        data = []
        for part_enum_item in Part:
            part_number_data_of_part = API.get_part_number_data(part_enum_item)
            data += part_number_data_of_part
        
        return data
    #!
    #!
    #!



    #!
    #!
    #!
    # получить данные о user_ratings для для таблицы pcpartpicker_user_ratings
    def get_user_rating_data(part: Part):
        part_data = API.get_data_of_part(part)

        data = []
        for block_key, block_data in part_data.items():
            key = None
            ratings_count = None
            average_rating = None

            five_star = None
            four_star = None
            three_star = None
            two_star = None
            one_star = None

            for item in block_data:
                if any(entry.get("Header") == "Main" for entry in item):
                    key = item[4]["Key"]
                
                if any(entry.get("Header") == "UserRatings" for entry in item):
                    for entry in item:
                        if "Name" in entry and "Value" in entry:
                            if entry["Name"] == "RatingsCount":
                                ratings_count = entry["Value"]
                            if entry["Name"] == "AverageRating":
                                average_rating = entry["Value"]
                            if entry["Name"] == "Rating":
                                five_star = entry["Value"]["5 Star"].replace("%", "")
                                four_star = entry["Value"]["4 Star"].replace("%", "")
                                three_star = entry["Value"]["3 Star"].replace("%", "")
                                two_star = entry["Value"]["2 Star"].replace("%", "")
                                one_star = entry["Value"]["1 Star"].replace("%", "")
            
            data.append([ key, ratings_count, average_rating, five_star, four_star, three_star, two_star, one_star ])
        
        return data

    # получить данные о user_ratings для для таблицы pcpartpicker_user_ratings для всех категорий
    def get_user_rating_data_of_all_parts():
        data = []
        for part_enum_item in Part:
            user_rating_data_of_part = API.get_user_rating_data(part_enum_item)
            data += user_rating_data_of_part
        
        return data
    #!
    #!
    #! 


    
    #!
    #!
    #! 
    def get_price_data(part: Part):
        part_data = API.get_data_of_part(part)
        params = ["MerchantLink", "MerchantName", "BasePrice", "PromoValue", "ShippingText", "ShippingLink", "TaxValue", "Availability", "FinalPrice", "LastUpdateTime"]

        data = []
        for block_key, block_data in part_data.items():
            key = None

            for item in block_data:
                if any(entry.get("Header") == "Main" for entry in item):
                    key = item[4]["Key"]
                
                if any(entry.get("Header") == "PriceData" for entry in item):
                    for entry in item:
                        params_values = []

                        for param in params:
                            if param in entry:
                                params_values.append(entry[param])

                        if len(params_values) == 0:
                            continue

                        if params_values[4] == '':
                            params_values[4] = None

                        if params_values[2] is not None:
                            base_price = float(params_values[2].replace("$", "").replace("+", "").replace("-", ""))
                        else:
                            base_price = None

                        if params_values[3] is not None:
                            promo_value = float(params_values[3].replace("$", "").replace("+", ""))
                        else:
                            promo_value = None

                        if params_values[8] is not None:
                            final_price = float(params_values[8].replace("$", "").replace("+", ""))
                        else:
                            final_price = None

                        data.append([ key, params_values[0], params_values[1], 
                                    base_price, promo_value, params_values[4], 
                                    params_values[5], params_values[6], params_values[7], 
                                    final_price, "$" ,params_values[9] ])
        
        return data

    def get_price_data_of_all_parts():
        data = []
        for part_enum_item in Part:
            price_data_of_part = API.get_price_data(part_enum_item)
            data += price_data_of_part
        
        return data
    #!
    #!
    #!

    #!
    #!
    #!
    # возвращает key, image_name, image_link
    def get_image_links_data(part: Part):
        part_data = API.get_data_of_part(part)

        data = []
        for block_key, block_data in part_data.items():
            key = None

            for item in block_data:
                if any(entry.get("Header") == "Main" for entry in item):
                    key = item[4]["Key"]
                
                if any(entry.get("Header") == "ImagesData" for entry in item):
                    for entry in item:
                        if "Name" in entry and "Value" in entry:
                            image_name = entry["Name"]
                            image_link = entry["Value"]
                            data.append([ key, image_name, image_link ])
        
        return data

    def get_image_links_data_of_all_parts():
        data = []
        for part_enum_item in Part:
            image_links_data_of_part = API.get_image_links_data(part_enum_item)
            data += image_links_data_of_part
        
        return data

    def get_image_data():
        image_links = API.get_image_links_data_of_all_parts()

        image_data = []
        for key, image_name, image_link in image_links:
            image_bytes = Images.get_image_from_file(image_name)
            image_data.append([ key, image_name, image_link, image_bytes ])

        return image_data
    #!
    #!
    #!


    # 
    #
    # попробовать реализовать handle для cpu
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

    def __get_local_entity_class_name(class_name: str):
        class_names_mapping = API.__get_part_mapping("class_names")
        for key, value in class_names_mapping.items():
            if key == class_name:
                return value

    def get_specification_data(part: Part) -> List:
        part_data = API.get_data_of_part(part)
        mapping = API.__get_part_mapping(part.value)
        
        class_name = API.__get_local_entity_class_name(part.value)
        my_instance = globals()[class_name]

        data = []
        for block_key, block_data in part_data.items():
            key = None

            parameters = {}

            for item in block_data:
                if any(entry.get("Header") == "Main" for entry in item):
                    key = item[4]["Key"]
                    parameters["key"] = key
                
                if any(entry.get("Header") == "SpecificationTable" for entry in item):
                    for entry in item:
                        if "Name" in entry and "Value" in entry:
                            for key, value in mapping.items():
                                if value == entry["Name"]:
                                    parameters[key] = entry["Value"]

            entity = my_instance(**parameters)
            data.append(entity)
        
        return data
            
    #!
    #!
    #!
    # метод для получение ссылок на комплектующие конкретной категории
    def get_links_of_part(part: Part):
        part = Part.get_part_enum(part.value)
        links = Links.get_links_from_json(part)

        return links
    
    # метод для получения всех ссылок на комплектующие
    def get_all_links():
        data = {}

        index = 0
        for part in Part:
            links = API.get_links_of_part(part)
            for link in links:
                data[index] = link
                index = index + 1

        return data
    #!
    #!
    #!



    #!
    #!
    #!
    # specification table - это всегда второй список в dict
    def __get_names_from_spec_table(blocks):
        names = [item.get('Name') for item in blocks[1] if 'Name' in item]
        return names

    # получение уникальнх названий параметров из таблицы specification table
    def get_unique_specification_names_of_part(part: Part):
        part_data = API.get_data_of_part(part)
        
        unique_specification_names = []
        for key, blocks in part_data.items():
            spec_table_names = API.__get_names_from_spec_table(blocks)
            for name in spec_table_names:
                if name not in unique_specification_names:
                    unique_specification_names.append(name)

        return unique_specification_names

    # сохранение уникальных параметров для конкретной категории в json
    def save_unique_params_to_json(part: Part, unique_specification_names: dict):
        current_directory = os.getcwd()
        file_path = current_directory + PARAMETERS_MAPPING_RELATIVE_PATH + str(part.value) + "_unique_names.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(unique_specification_names, json_file, indent=4, ensure_ascii=False)

    # сохранение всех уникальных параметров в соответствующие категории json файлы
    def save_all_unique_specification_names_to_json():
        for part in Part:
            unique_names = API.get_unique_specification_names_of_part(part)
            API.save_unique_params_to_json(part, unique_names)
    #!
    #!
    #!

    #!
    #!
    #!
    # метод для получения кратких сведений о каждом параметре
    def get_params_summary_data_of_part(part: Part):
        part_data = API.get_data_of_part(part)

        params_summary_data = {}  # Создаем словарь для хранения уникальных имен, типов данных и максимальных значений
        unique_params = {}
        params_summary_data["category_length"] = len(part_data)
        # Перебираем блоки данных
        for block_key, block_data in part_data.items():
            for item in block_data:
                # Ищем блок "SpecificationTable" внутри блока данных
                if any(entry.get("Header") == "SpecificationTable" for entry in item):
                    # Итерируем по элементам блока "SpecificationTable"
                    for entry in item:
                        if "Name" in entry:
                            name = entry["Name"]
                            if name not in params_summary_data:
                                params_summary_data[name] = {"types": {}, "max_value": None, "unique_values": [], "unique_values_count": 0}
                                unique_params[name] = { "unique_values": [], "unique_values_count": 0 }
                        if "Value" in entry:
                            value = entry["Value"]
                            value_type = type(value).__name__

                            # Добавляем тип данных в множество уникальных типов данных
                            if value_type not in params_summary_data[name]["types"]:
                                params_summary_data[name]["types"][value_type] = 0
                            params_summary_data[name]["types"][value_type] += 1

                            # Проверяем и обновляем максимальное значение
                            if (isinstance(value, (int, float)) and (params_summary_data[name]["max_value"] is None or value > params_summary_data[name]["max_value"])) and isinstance(params_summary_data[name]["max_value"], list) == False:
                                params_summary_data[name]["max_value"] = value
                            elif (isinstance(value, str) and (params_summary_data[name]["max_value"] is None or len(value) > len(params_summary_data[name]["max_value"]))) and isinstance(params_summary_data[name]["max_value"], list) == False:
                                params_summary_data[name]["max_value"] = value
                            elif isinstance(value, list) and (params_summary_data[name]["max_value"] is None or len(value) > len(params_summary_data[name]["max_value"])):
                                params_summary_data[name]["max_value"] = value

                            # если больше 10 значений то пишем количество уникальный значений
                            if value not in unique_params[name]["unique_values"]:
                                if len(params_summary_data[name]["unique_values"]) > 10:
                                    pass
                                else:
                                    params_summary_data[name]["unique_values"].append(value)
                                
                                unique_params[name]["unique_values"].append(value)
                                params_summary_data[name]["unique_values_count"] += 1

        return params_summary_data

    # метод для сохранения кратких сведений каждого параметра для одной категории
    # комплектующих
    def save_params_summary_data_to_json(part: Part, params_summary_data: dict):
        current_directory = os.getcwd()
        file_path = current_directory + PARAMETERS_MAPPING_RELATIVE_PATH + str(part.value) + "_unique_names.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(params_summary_data, json_file, indent=4, ensure_ascii=False)

    # сохранение всех кратких сведений
    def save_all_params_summary_data_to_json():
        for part in Part:
            params_summary_data = API.get_params_summary_data_of_part(part)
            API.save_params_summary_data_to_json(part, params_summary_data)
    #!
    #!
    #!



    #!
    #!
    #!
    # получить все значения параметра
    def get_all_values_of_parameter(part: Part, header_name: str, parameter_name: str) -> list:
        part_data = API.get_data_of_part(part)

        values = []
        for block_key, block_data in part_data.items():
            for item in block_data:
                if any(entry.get("Header") == header_name for entry in item):
                    for entry in item:
                        if "Name" in entry and "Value" in entry:
                            name = entry["Name"]

                            if name == parameter_name:
                                value = entry["Value"]

                                values.append(value)
        return values

    # получить только уникальные значения параметра
    def get_unique_values_of_parameter(part: Part, header_name: str, parameter_name: str) -> list:
        part_data = API.get_data_of_part(part)

        values = []
        for block_key, block_data in part_data.items():
            for item in block_data:
                if any(entry.get("Header") == header_name for entry in item):
                    for entry in item:
                        if "Name" in entry and "Value" in entry:
                            name = entry["Name"]

                            if name == parameter_name:
                                value = entry["Value"]

                                if value not in values:
                                    values.append(value)
        return values
    #!
    #!
    #!



    #!
    #!
    #!
    def get_parameters_summary_data(header_name: str):
        unique_params = {}
        params_summary_data = {}
        params_summary_data["category_length"] = 0
        for part in Part:
            part_data = API.get_part_data(part)
            params_summary_data["category_length"] += len(part_data)
            # Перебираем блоки данных
            for block_key, block_data in part_data.items():
                for item in block_data:
                    # Ищем блок "SpecificationTable" внутри блока данных
                    if any(entry.get("Header") == header_name for entry in item):
                        # Итерируем по элементам блока "SpecificationTable"
                        for entry in item:
                            if "Name" in entry:
                                name = entry["Name"]
                                if name not in params_summary_data:
                                    params_summary_data[name] = {"types": {}, "count": 0, "max_value": None, "unique_values": [], "unique_values_count": 0}
                                    unique_params[name] = { "unique_values": [], "unique_values_count": 0 }
                            if "Value" in entry:
                                value = entry["Value"]
                                value_type = type(value).__name__

                                # Добавляем тип данных в множество уникальных типов данных
                                if value_type not in params_summary_data[name]["types"]:
                                    params_summary_data[name]["types"][value_type] = 0
                                params_summary_data[name]["types"][value_type] += 1

                                params_summary_data[name]["count"] += 1

                                # Проверяем и обновляем максимальное значение
                                if (isinstance(value, (int, float)) and (params_summary_data[name]["max_value"] is None or value > params_summary_data[name]["max_value"])) and isinstance(params_summary_data[name]["max_value"], list) == False:
                                    params_summary_data[name]["max_value"] = value
                                elif (isinstance(value, str) and (params_summary_data[name]["max_value"] is None or len(value) > len(params_summary_data[name]["max_value"]))) and isinstance(params_summary_data[name]["max_value"], list) == False:
                                    params_summary_data[name]["max_value"] = value
                                elif isinstance(value, list) and (params_summary_data[name]["max_value"] is None or len(value) > len(params_summary_data[name]["max_value"])):
                                    params_summary_data[name]["max_value"] = value

                                # если больше 50 значений то пишем количество уникальный значений
                                if value not in unique_params[name]["unique_values"]:
                                    if len(params_summary_data[name]["unique_values"]) > 25:
                                        pass
                                    else:
                                        params_summary_data[name]["unique_values"].append(value)

                                    unique_params[name]["unique_values"].append(value)
                                    params_summary_data[name]["unique_values_count"] += 1

        return params_summary_data
    
    def save_all_parameters_summary_data_to_json(header_name: str):
        params_summary_data = API.get_parameters_summary_data(header_name)
        API.save_params_summary_data_to_json(header_name, params_summary_data)
    #!
    #!
    #!

    
    
    #!
    #!
    #!
    def get_parameters_summary_price_data():
        params = ["MerchantLink", "MerchantName", "BasePrice", "PromoValue", "ShippingText", "ShippingLink", "TaxValue", "Availability", "FinalPrice", "LastUpdateTime"]

        params_summary_data = {}
        params_summary_data["category_length"] = 0
        for part in Part:
            part_data = API.get_part_data(part.value)
            params_summary_data["category_length"] += len(part_data)
            # Перебираем блоки данных
            for block_key, block_data in part_data.items():
                for item in block_data:
                    if any(entry.get("Header") == "PriceData" for entry in item):
                        for entry in item:
                            for param in params:
                                if param in entry:
                                    name = param
                                    if name not in params_summary_data:
                                        params_summary_data[name] = {"types": {}, "count": 0, "max_value": None, "unique_values": [], "unique_values_count": 0}

                                    value = entry[param]
                                    value_type = type(value).__name__

                                    # Добавляем тип данных в множество уникальных типов данных
                                    if value_type not in params_summary_data[name]["types"]:
                                        params_summary_data[name]["types"][value_type] = 0
                                    params_summary_data[name]["types"][value_type] += 1

                                    params_summary_data[name]["count"] += 1

                                    # Проверяем и обновляем максимальное значение
                                    if (isinstance(value, (int, float)) and (params_summary_data[name]["max_value"] is None or value > params_summary_data[name]["max_value"])) and isinstance(params_summary_data[name]["max_value"], list) == False:
                                        params_summary_data[name]["max_value"] = value
                                    elif (isinstance(value, str) and (params_summary_data[name]["max_value"] is None or len(value) > len(params_summary_data[name]["max_value"]))) and isinstance(params_summary_data[name]["max_value"], list) == False:
                                        params_summary_data[name]["max_value"] = value
                                    elif isinstance(value, list) and (params_summary_data[name]["max_value"] is None or len(value) > len(params_summary_data[name]["max_value"])):
                                        params_summary_data[name]["max_value"] = value

                                    # если больше 50 значений то пишем количество уникальный значений
                                    if value not in params_summary_data[name]["unique_values"]:
                                        if len(params_summary_data[name]["unique_values"]) > 25:
                                            pass
                                        else:
                                            params_summary_data[name]["unique_values"].append(value)
                                        params_summary_data[name]["unique_values_count"] += 1

        return params_summary_data
    
    def save_all_parameters_summary_price_data_to_json():
        params_summary_data = API.get_parameters_summary_price_data()
        API.save_params_summary_data_to_json("PriceData", params_summary_data)
    #!
    #!
    #!

    def check_includes_cooler():
        values = API.get_all_values_of_parameter("cpu", "SpecificationTable", "Includes Cooler")
        values1 = API.get_all_values_of_parameter("cpu", "SpecificationTable", "Includes CPU Cooler")

        if values == values1:
            print("Списки соответствуют.")
        else:
            print("Списки не соответствуют.")