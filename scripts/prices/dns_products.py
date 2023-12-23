import logging
import time
from src.prices.dns.Products import Products

LOG_PATH = "data\\logs\\dns_products.log"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("dns_products")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

parser = Products(logger)
with parser:
    start_time = time.time()

    # всего должно быть +- 3569
    # напарсило 4608, примерно 1000 лишних
    data = parser.save_parts_links()
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Метод выполнился за {execution_time:.2f} секунд")
