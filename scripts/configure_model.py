import json
import os
import time
from src.configure.ConfigureModel import ConfigureModel

start_time = time.time()
model = ConfigureModel()
combinations = model.parse_all_combinations_of_main_configure()
end_time = time.time()
execution_time = end_time - start_time
print(f"Метод выполнился за {execution_time} секунд.")

current_directory = os.getcwd()
current_file_path = current_directory + "\\data\\configure\\"

with open(current_file_path + 'main_combinations.json', 'w', encoding="utf-8") as json_file:
    json.dump(combinations, json_file, indent=4)