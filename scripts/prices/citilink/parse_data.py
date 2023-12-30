import logging
import time
from src.prices.citilink.PriceParser import PriceParser

LOG_PATH = "data\\logs\\citilink_prices.log"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("citilink")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

parser = PriceParser(logger)
with parser:
    start_time = time.time()

    data = parser.parse_all_data()
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Метод выполнился за {execution_time:.2f} секунд")
