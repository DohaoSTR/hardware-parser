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
for key, value in compatible.items():
    if value["similarity_percentage"] >= 30:
        metric: UserBenchmarkMetric = ub_mapper.session.query(UserBenchmarkMetric).filter_by(part_id = value["ub_id"]).first()

        if metric != None:
            new_metrics[key] = {
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

for key, value in compatible.items():   
    found = any(value["ppp_id"] == entry.get("ppp_id") for entry in new_metrics.values())
    if found == False:    
        priceEntities: PcPartPickerPriceEntity = ppp_mapper.session.query(PcPartPickerPriceEntity).filter_by(part_id = value["ppp_id"]).all()
        
        averagePrice = 0
        for priceEntity in priceEntities:
            averagePrice += priceEntity.base_price

        if averagePrice != 0:
            averagePrice = averagePrice / len(priceEntities)

        if averagePrice == 0:
            new_metrics[key] = {
            "average_price_null": None,
            "gaming_percentage": None,
            "desktop_percentage": None,
            "workstation_percentage": None,

            "ub_id": value["ub_id"],
            "ub_name": value["ub_name"],
            "ub_part_number": value["ub_part_number"],
            "ppp_id": value["ppp_id"],
            "ppp_name": value["ppp_name"],
            "ppp_part_number": value["ppp_part_number"],
        }
        else:
            part: PcPartPickerPartEntity = ppp_mapper.session.query(PcPartPickerPartEntity).filter_by(id = value["ppp_id"]).first()
            
            values = {}
            for new_metric_key, new_metric_value in new_metrics.items():
                new_part: PcPartPickerPartEntity = ppp_mapper.session.query(PcPartPickerPartEntity).filter_by(id = new_metric_value["ppp_id"], 
                                                                                                              part_type = part.part_type).first()
                if new_part == None:
                    pass
                else:
                    newPricesEntities: PcPartPickerPriceEntity = ppp_mapper.session.query(PcPartPickerPriceEntity).filter_by(part_id = new_part.part_type).all()

                    newAveragePrice = 0
                    for priceEntity in newPricesEntities:
                        newAveragePrice += priceEntity.base_price

                    if newAveragePrice != 0:
                        newAveragePrice = newAveragePrice / len(newPricesEntities)

                    if newAveragePrice == 0:
                        pass
                    else:
                        values[new_metric_value["ub_id"]] = newAveragePrice

            if len(values) > 0:
                closest_key = min(values, key=lambda k: abs(values[k] - averagePrice))
            else: 
                new_metrics[key] = {
                    "closest_key < 0": None,
                    "gaming_percentage": None,
                    "desktop_percentage": None,
                    "workstation_percentage": None,

                    "ub_id": value["ub_id"],
                    "ub_name": value["ub_name"],
                    "ub_part_number": value["ub_part_number"],
                    "ppp_id": value["ppp_id"],
                    "ppp_name": value["ppp_name"],
                    "ppp_part_number": value["ppp_part_number"],
                }
                break

            if closest_key != None:
                metric = ub_mapper.session.query(UserBenchmarkMetric).filter_by(part_id = closest_key).first()

                if metric != None:
                    new_metrics[key] = {
                        "closest_price": "YES",
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
                    break
                else:
                    new_metrics[key] = {
                        "metric": None,
                        "gaming_percentage": None,
                        "desktop_percentage": None,
                        "workstation_percentage": None,

                        "ub_id": value["ub_id"],
                        "ub_name": value["ub_name"],
                        "ub_part_number": value["ub_part_number"],
                        "ppp_id": value["ppp_id"],
                        "ppp_name": value["ppp_name"],
                        "ppp_part_number": value["ppp_part_number"],
                    }
                    break
            else:
                new_metrics[key] = {
                    "closest_key": None,
                    "gaming_percentage": None,
                    "desktop_percentage": None,
                    "workstation_percentage": None,

                    "ub_id": value["ub_id"],
                    "ub_name": value["ub_name"],
                    "ub_part_number": value["ub_part_number"],
                    "ppp_id": value["ppp_id"],
                    "ppp_name": value["ppp_name"],
                    "ppp_part_number": value["ppp_part_number"],
                }
                break

current_directory = os.getcwd()
path = current_directory + "\\data\\ppp_ub_metrics.json"
with open(path, 'w', encoding='utf-8') as json_file:
    json.dump(new_metrics, json_file, indent=4, ensure_ascii=False)

print("Count " + str(len(new_metrics)))

# есть 26к совпадений