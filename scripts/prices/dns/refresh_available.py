import logging
import time
from src.prices.dns.db_mapper.DatabaseMapper import DatabaseMapper

from src.prices.dns.ProductsParser import ProductsParser

LOG_PATH = "data\\logs\\dns_refresh_statuses.log"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("dns_refresh_statuses")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def map_all_statuses():
    parser = ProductsParser(logger)
    with parser:
        start_time = time.time()

        data = parser.map_all_statuses()

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Метод выполнился за {execution_time:.2f} секунд")

map_all_statuses()