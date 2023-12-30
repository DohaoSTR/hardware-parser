import logging
import time

from src.prices.dns.ProductsParser import ProductsParser
from src.prices.dns.db_mapper.Mapper import DatabaseMapper

LOG_PATH = "data\\logs\\dns_refresh_prices.log"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("dns_refresh_prices")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

start_time = time.time()
parser = ProductsParser(logger)
mapper = DatabaseMapper(logger)

with parser:
    data = parser.parse_all_microdata()
with mapper:
    mapper.add_prices(data)

end_time = time.time()
execution_time = end_time - start_time
print(f"Метод выполнился за {execution_time:.2f} секунд")