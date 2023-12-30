import logging
import time

from src.prices.dns.ProductsParser import ProductsParser

LOG_PATH = "data\\logs\\dns_uid_parser.log"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("dns_uid_parser")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_products_data():
    parser = ProductsParser(logger)
    with parser:
        start_time = time.time()

        parser.get_all_data()

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Метод выполнился за {execution_time:.2f} секунд")
        
def get_all_microdata():
    parser = ProductsParser(logger)
    with parser:
        start_time = time.time()

        data = parser.parse_all_microdata()

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Метод выполнился за {execution_time:.2f} секунд")

get_products_data()
get_all_microdata()