import logging
import time

from src.prices.citilink.PriceParser import PriceParser
from src.prices.citilink.db_mapper.DatabaseMapper import DatabaseMapper

LOG_PATH = "data\\logs\\citilink_mapper_main.log"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("citilink_mapper_main")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def add_products_data():
    parser = PriceParser(logger)
    mapper = DatabaseMapper(logger)

    start_time = time.time()

    with parser:
        data = parser.get_data()

    with mapper:
        mapper.add_products_data(data)
        
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Метод выполнился за {execution_time:.2f} секунд")

def add_price_data():
    parser = PriceParser(logger)
    mapper = DatabaseMapper(logger)

    start_time = time.time()

    with parser:
        data = parser.get_data()

    with mapper:
        mapper.add_price_data(data)
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Метод выполнился за {execution_time:.2f} секунд")

def add_available_data():
    parser = PriceParser(logger)
    mapper = DatabaseMapper(logger)

    start_time = time.time()

    with parser:
        data = parser.get_data()

    with mapper:
        mapper.add_available_data(data)
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Метод выполнился за {execution_time:.2f} секунд")

add_products_data()
add_price_data()
add_available_data()