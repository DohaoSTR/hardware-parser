import json
import os

def get_dns_pcpartpicker():
    current_directory = os.getcwd()
    file_path = current_directory + "\\data\\dns_pcpartpicker_compatible.json"

    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    items = {}
    index = 0
    for key, value in data.items():
        if value["similarity_percentage"] >= 30:
            dns_id = value["dns_id"]
            ppp_id = value["ppp_id"]

            items[index] = {
                "dns_id": dns_id,
                "ppp_id": ppp_id
            }
            index += 1

    return items

def get_citilink_pcpartpicker():
    current_directory = os.getcwd()
    file_path = current_directory + "\\data\\citilink_ppp_compatible.json"

    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    items = {}
    index = 0
    for key, value in data.items():
        if value["similarity_percentage"] >= 30:
            citilink_id = value["citilink_id"]
            ppp_id = value["ppp_id"]

            items[index] = {
                "citilink_id": citilink_id,
                "ppp_id": ppp_id
            }
            index += 1

    return items

def get_pcpartpicker_userbenchmark():
    current_directory = os.getcwd()
    file_path = current_directory + "\\data\\ppp_ub_compatible.json"

    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    items = {}
    index = 0
    for key, value in data.items():
        if value["similarity_percentage"] >= 30:
            ub_id = value["ub_id"]
            ppp_id = value["ppp_id"]

            items[index] = {
                "ub_id": ub_id,
                "ppp_id": ppp_id
            }
            index += 1

    return items

def get_metrics():
    current_directory = os.getcwd()
    file_path = current_directory + "\\data\\ppp_ub_metrics.json"

    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    items = {}
    index = 0
    for key, value in data.items():
        gaming_percentage = value["gaming_percentage"]
        desktop_percentage = value["desktop_percentage"]
        workstation_percentage = value["workstation_percentage"]
        ppp_id = value["ppp_id"]

        if gaming_percentage is not None or desktop_percentage is not None or workstation_percentage is not None:
            items[index] = {
                "gaming_percentage": gaming_percentage,
                "desktop_percentage": desktop_percentage,
                "workstation_percentage": workstation_percentage,
                "ppp_id": ppp_id
            }
            index += 1

    return items