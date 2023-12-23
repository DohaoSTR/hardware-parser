import logging
import time

from src.prices.dns.UIDParser import UIDParser

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

parser = UIDParser(logger)
with parser:
    start_time = time.time()

    data = parser.get_product_data("https://www.dns-shop.ru/product/c3c60e33a1982ff1/processor-amd-fx-4300-box/")
    print(data)
    print(len(data))
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Метод выполнился за {execution_time:.2f} секунд")