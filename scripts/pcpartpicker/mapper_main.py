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

def add_all_main_data():
    db.add_all_parts_main_data()
    db.add_all_part_number_data()
    db.add_all_user_rating_data()
    db.add_all_price_data()
    db.add_all_image_link_data()
    db.add_all_image_data()### erDataBase. Метод add_all_image_data. Ошибка - (MySQLdb.OperationalError) (2013, 'Lost connection to server during query')
                           ###(Background on this error at: https://sqlalche.me/e/20/e3q8)

def add_all_parts_data():
    db.add_all_cpu_data()
    db.add_all_gpu_data()
    db.add_all_memory_data()
    db.add_all_motherboard_data()
    db.add_all_internal_hard_drive_data()
    db.add_all_case_data()
    db.add_all_case_fan_data()
    db.add_all_cpu_cooler_data()
    db.add_all_power_supply()

add_all_main_data()
add_all_parts_data()