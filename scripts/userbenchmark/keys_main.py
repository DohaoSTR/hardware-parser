import logging

from src.userbenchmark.UserBenchmarkPartKeys import UserBenchmarkPartKeys

LOG_PATH = "data\\userbenchmark\\logs\\keys_main.log"

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                encoding='utf-8')
logger = logging.getLogger("keys_main")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

parser = UserBenchmarkPartKeys(logger)
parser.get_all_part_keys()