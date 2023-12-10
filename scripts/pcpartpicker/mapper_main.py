from src.pcpartpicker.DatabaseMapper import DatabaseMapper

import logging

LOG_PATH = "data\\pcpartpicker\\logs\\map_data_to_db.log"

logging.basicConfig(level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
encoding='utf-8')
logger = logging.getLogger("map_data_to_db")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

db = DatabaseMapper(logger)
db.add_all_power_supply()