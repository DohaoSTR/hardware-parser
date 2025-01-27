from src.userbenchmark.mapper.DatabaseMapper import DatabaseMapper

import logging

LOG_PATH = "data\\userbenchmark\\logs\\mapper_main.log"

logging.basicConfig(level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
encoding='utf-8')
logger = logging.getLogger("mapper_main")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

mapper = DatabaseMapper(logger)

def add_all_data_without_fps():
    mapper.add_parts()
    mapper.add_games()
    mapper.add_parts_keys()
    mapper.add_compare_keys()
    mapper.add_metrics()
    mapper.add_all_parts()

def add_fps_data():
    mapper.add_unadded_fps_data()

#add_all_data_without_fps()
#add_fps_data()
mapper.add_game_images()