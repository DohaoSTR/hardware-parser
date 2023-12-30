import logging
import time

from src.prices.dns.db_mapper.Mapper import DatabaseMapper
from src.prices.dns.ProductsParser import ProductsParser

LOG_PATH = "data\\logs\\dns_mapper.log"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("dns_mapper")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def products_data_mapper():
    mapper = DatabaseMapper(logger)
    parser = ProductsParser(logger)
    with parser:
        start_time = time.time()

        data = parser.get_data()
        microdata = parser.get_all_microdata()
        mapper.add_products_data(microdata, data)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Метод выполнился за {execution_time:.2f} секунд")

def prices_mapper():
    mapper = DatabaseMapper(logger)
    parser = ProductsParser(logger)
    with parser:
        start_time = time.time()

        microdata = parser.get_all_microdata()
        mapper.add_prices(microdata)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Метод выполнился за {execution_time:.2f} секунд")

products_data_mapper()
prices_mapper()