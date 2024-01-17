import json
import os

from src.userbenchmark.mapper.db_entities.PartEntity import PartEntity as UserBenchmarkPartEntity
from src.userbenchmark.mapper.db_entities.Metric import Metric as UserBenchmarkMetric
from src.userbenchmark.mapper.DatabaseMapper import DatabaseMapper as UserBenchmarkMapper

from src.pcpartpicker.db_entities.PartEntity import PartEntity as PcPartPickerPartEntity
from src.pcpartpicker.DatabaseMapper import DatabaseMapper as PcPartPickerMapper
from src.pcpartpicker.db_entities.PriceEntity import PriceEntity as PcPartPickerPriceEntity

ub_mapper = UserBenchmarkMapper()
ub_parts = ub_mapper.session.query(UserBenchmarkPartEntity).all()

ppp_mapper = PcPartPickerMapper()
ppp_parts = ppp_mapper.session.query(PcPartPickerPartEntity).all()

current_directory = os.getcwd()
file_path = current_directory + "\\data\\ppp_ub_compatible.json"

with open(file_path, 'r', encoding='utf-8') as json_file:
    compatible = json.load(json_file)

new_metrics = {}
index = 1
for key, value in compatible.items():
    if value["similarity_percentage"] >= 30:
        metric: UserBenchmarkMetric = ub_mapper.session.query(UserBenchmarkMetric).filter_by(part_id = value["ub_id"]).first()

        if metric != None:
            new_metrics[index] = {
                "gaming_percentage": metric.gaming_percentage,
                "desktop_percentage": metric.desktop_percentage,
                "workstation_percentage": metric.workstation_percentage,

                "ub_id": value["ub_id"],
                "ub_name": value["ub_name"],
                "ub_part_number": value["ub_part_number"],

                "ppp_id": value["ppp_id"],
                "ppp_name": value["ppp_name"],
                "ppp_part_number": value["ppp_part_number"],
            }
            print(index)
            index += 1
    
current_directory = os.getcwd()
path = current_directory + "\\data\\ppp_ub_metrics.json"
with open(path, 'w', encoding='utf-8') as json_file:
    json.dump(new_metrics, json_file, indent=4, ensure_ascii=False)

print("Count " + str(len(new_metrics)))
# есть 26к совпадений