import json
import os

import Levenshtein

from src.prices.citilink.db_mapper.Product import Product as CitilinkProduct
from src.prices.citilink.db_mapper.DatabaseMapper import DatabaseMapper as CitilinkDBMapper

from src.prices.dns.db_mapper.Product import Product as DNSProduct
from src.prices.dns.db_mapper.DatabaseMapper import DatabaseMapper as DNSDBMapper

from src.pcpartpicker.db_entities.PartEntity import PartEntity as PcPartPickerPartEntity
from src.pcpartpicker.DatabaseMapper import DatabaseMapper as PcPartPickerMapper

from src.userbenchmark.mapper.db_entities.PartEntity import PartEntity as UserBenchmarkPartEntity
from src.userbenchmark.mapper.DatabaseMapper import DatabaseMapper as UserBenchmarkMapper

def levenshtein_ratio(s1, s2):
    distance = Levenshtein.distance(s1, s2)
    max_len = max(len(s1), len(s2))
    similarity_ratio = round((1 - distance / max_len) * 100)
    return similarity_ratio

#ppp_mapper = PcPartPickerMapper()
#ppp_parts = ppp_mapper.session.query(PcPartPickerPartEntity).all()

ub_mapper = UserBenchmarkMapper()
ub_parts = ub_mapper.session.query(UserBenchmarkPartEntity).all()

citilink_mapper = CitilinkDBMapper()
citilink_parts = citilink_mapper.session.query(CitilinkProduct).all()

index = 0
items = {}
for citilink_part in citilink_parts:
    best_similarity = 0
    best_dns_part = None
    for dns_part in dns_parts:
        similarity_percentage = levenshtein_ratio(citilink_part.name, str(dns_part.name).replace("[", "").replace("]", ""))
        if similarity_percentage > 75 and similarity_percentage > best_similarity:
            best_similarity = similarity_percentage
            best_dns_part = dns_part

    if best_dns_part is not None:
        items[citilink_part.id] = { 
            "similarity_percentage": best_similarity,
            "citilink_id": citilink_part.id,
            "dns_id": best_dns_part.uid,
            "citilink_name": citilink_part.name,
            "dns_name": best_dns_part.name,
            "dns_part_number": best_dns_part.part_number,
            "citilink_part_number": citilink_part.part_number
        }

indexed_items = {}
new_index = 0
for index_items, item in items.items():
    indexed_items[new_index] = item
    new_index += 1

current_directory = os.getcwd()
path = current_directory + "\\data\\compatible_levenshtein_76.json"
with open(path, 'w', encoding='utf-8') as json_file:
    json.dump(indexed_items, json_file, indent=4, ensure_ascii=False)