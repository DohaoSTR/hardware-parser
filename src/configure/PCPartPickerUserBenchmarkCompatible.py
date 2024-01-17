import json
import os

import Levenshtein

from src.userbenchmark.mapper.db_entities.PartEntity import PartEntity as UserBenchmarkPartEntity
from src.userbenchmark.mapper.DatabaseMapper import DatabaseMapper as UserBenchmarkMapper

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

ub_mapper = UserBenchmarkMapper()
ub_parts = ub_mapper.session.query(UserBenchmarkPartEntity).all()

items = {}
index = 0
for ppp_part in ppp_parts:
    index += 1
    print(index)

    part_numbers = ppp_mapper.session.query(PartNumberEntity).filter_by(part_id = ppp_part.id).all()

    found_match = False
    best_ub_part = None
    best_part_number = None
    for part_number_entity in part_numbers:    
        for ub_part in ub_parts:
            if ub_part.part_number == part_number_entity.part_number:  
                best_ub_part = ub_part    
                best_part_number = part_number_entity.part_number        
                found_match = True
                break

        if found_match == True:
            break
    
    if found_match == False:
        best_similarity = 0
        best_ub_part = None
        for ub_part in ub_parts:
            similarity_percentage = levenshtein_ratio(ppp_part.name, str(ub_part.model).replace("[", "").replace("]", ""))
            if similarity_percentage > best_similarity:
                best_similarity = similarity_percentage
                best_ub_part = ub_part

        if best_ub_part == None:
            items[index] = { 
                "similarity_percentage": best_similarity,
                "ub_id": None,
                "ub_name": None,
                "ub_part_number": None,
                "ppp_id": ppp_part.id,
                "ppp_name": ppp_part.name,
                "ppp_part_number": None
            }
        else:
            items[index] = { 
                "similarity_percentage": best_similarity,
                "ub_id": best_ub_part.id,
                "ub_name": best_ub_part.model,
                "ub_part_number": best_ub_part.part_number,
                "ppp_id": ppp_part.id,
                "ppp_name": ppp_part.name,
                "ppp_part_number": None
            }
    else:
        items[index] = { 
            "similarity_percentage": 100,
            "ub_id": best_ub_part.id,
            "ub_name": best_ub_part.model,
            "ub_part_number": best_ub_part.part_number,
            "ppp_id": ppp_part.id,
            "ppp_name": ppp_part.name,
            "ppp_part_number": best_part_number,
        }

current_directory = os.getcwd()
path = current_directory + "\\data\\ppp_ub_compatible.json"
with open(path, 'w', encoding='utf-8') as json_file:
    json.dump(items, json_file, indent=4, ensure_ascii=False)

print("Count " + str(len(items)))

# ub - 5107