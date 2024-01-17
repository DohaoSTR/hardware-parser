import json
import os
import re

import Levenshtein

from src.prices.citilink.db_mapper.Product import Product as CitilinkProduct
from src.prices.citilink.db_mapper.DatabaseMapper import DatabaseMapper as CitilinkDBMapper

from src.pcpartpicker.db_entities.PartEntity import PartEntity as PcPartPickerPartEntity
from src.pcpartpicker.db_entities.PartNumberEntity import PartNumberEntity as PartNumberEntity
from src.pcpartpicker.DatabaseMapper import DatabaseMapper as PcPartPickerMapper

def levenshtein_ratio(s1, s2):
    distance = Levenshtein.distance(s1, s2)
    max_len = max(len(s1), len(s2))
    similarity_ratio = round((1 - distance / max_len) * 100)
    return similarity_ratio

ppp_mapper = PcPartPickerMapper()
ppp_parts = ppp_mapper.session.query(PcPartPickerPartEntity).all()

citilink_mapper = CitilinkDBMapper()
citilink_parts = citilink_mapper.session.query(CitilinkProduct).all()

items = {}
index = 0
for ppp_part in ppp_parts:
    index += 1
    print(index)

    part_numbers = ppp_mapper.session.query(PartNumberEntity).filter_by(part_id = ppp_part.id).all()

    found_match = False
    best_citilink_part = None
    best_part_number = None
    for part_number_entity in part_numbers:
        for citilink_part in citilink_parts:
            if citilink_part.part_number == part_number_entity.part_number:
                best_citilink_part = citilink_part
                best_part_number = part_number_entity.part_number
                found_match = True
                break

        if found_match == True:
            break
    
    if found_match == False:
        best_similarity = 0
        best_citilink_part = None
        for citilink_part in citilink_parts:
            result_string = re.sub(r'\[.*?\]', '', citilink_part.name)
            similarity_percentage = levenshtein_ratio(ppp_part.name, str(result_string))
            if similarity_percentage > best_similarity:
                best_similarity = similarity_percentage
                best_citilink_part = citilink_part

        if best_citilink_part == None:
            items[index] = { 
                "similarity_percentage": best_similarity,
                "citilink_id": None,
                "citilink_name": None,
                "citilink_part_number": None,
                "ppp_id": ppp_part.id,
                "ppp_name": ppp_part.name,
                "ppp_part_number": None
            }
        else:
            items[index] = { 
                "similarity_percentage": best_similarity,
                "citilink_id": best_citilink_part.id,
                "citilink_name": best_citilink_part.name,
                "citilink_part_number": best_citilink_part.part_number,
                "ppp_id": ppp_part.id,
                "ppp_name": ppp_part.name,
                "ppp_part_number": None
            }
    else:
        items[index] = { 
            "similarity_percentage": 100,
            "citilink_id": best_citilink_part.id,
            "citilink_name": best_citilink_part.name,
            "citilink_part_number": best_citilink_part.part_number,
            "ppp_id": ppp_part.id,
            "ppp_name": ppp_part.name,
            "ppp_part_number": best_part_number,
        }

current_directory = os.getcwd()
path = current_directory + "\\data\\citilink_ppp_compatible.json"
with open(path, 'w', encoding='utf-8') as json_file:
    json.dump(items, json_file, indent=4, ensure_ascii=False)

print("Count " + str(len(items)))

# sitilink 2633