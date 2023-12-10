from src.userbenchmark.mapper.UserBenchmarkToDBMapper import UserBenchmarkToDBMapper

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

mapper = UserBenchmarkToDBMapper(logger)
mapper.add_unadded_fps_data()