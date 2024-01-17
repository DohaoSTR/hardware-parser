import json
import os

import Levenshtein

from src.prices.dns.db_mapper.Product import Product as DNSProduct
from src.prices.dns.db_mapper.DatabaseMapper import DatabaseMapper as DNSDBMapper

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

dns_mapper = DNSDBMapper()
dns_parts = dns_mapper.session.query(DNSProduct).all()

items = {}
index = 0
for ppp_part in ppp_parts:
    index += 1
    print(index)

    part_numbers = ppp_mapper.session.query(PartNumberEntity).filter_by(part_id = ppp_part.id).all()

    found_match = False
    dns_part_best = None
    best_part_number = None
    for part_number_entity in part_numbers:    
        for dns_part in dns_parts:
            if dns_part.part_number == part_number_entity.part_number:  
                dns_part_best = dns_part    
                best_part_number = part_number_entity.part_number        
                found_match = True
                break

        if found_match == True:
            break
    
    if found_match == False:
        best_similarity = 0
        best_dns_part = None
        for dns_part in dns_parts:
            similarity_percentage = levenshtein_ratio(ppp_part.name, str(dns_part.name).replace("[", "").replace("]", ""))
            if similarity_percentage > best_similarity:
                best_similarity = similarity_percentage
                best_dns_part = dns_part

        if best_dns_part == None:
            items[index] = { 
                "similarity_percentage": best_similarity,
                "dns_id": None,
                "dns_name": None,
                "dns_part_number": None,
                "ppp_id": ppp_part.id,
                "ppp_name": ppp_part.name,
                "ppp_part_number": None
            }
        else:
            items[index] = { 
                "similarity_percentage": best_similarity,
                "dns_id": best_dns_part.uid,
                "dns_name": best_dns_part.name,
                "dns_part_number": best_dns_part.part_number,
                "ppp_id": ppp_part.id,
                "ppp_name": ppp_part.name,
                "ppp_part_number": None
            }
    else:
        items[index] = { 
            "similarity_percentage": 100,
            "dns_id": dns_part_best.uid,
            "dns_name": dns_part_best.name,
            "dns_part_number": dns_part_best.part_number,
            "ppp_id": ppp_part.id,
            "ppp_name": ppp_part.name,
            "ppp_part_number": best_part_number,
        }

current_directory = os.getcwd()
path = current_directory + "\\data\\dns_pcpartpicker_compatible.json"
with open(path, 'w', encoding='utf-8') as json_file:
    json.dump(items, json_file, indent=4, ensure_ascii=False)

print("Count " + str(len(items)))

# 4206