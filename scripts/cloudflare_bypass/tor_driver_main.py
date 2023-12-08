from src.cloudflare_bypass.CloudflareTorDriver import CloudflareTorDriver

import logging
import time

from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
encoding='utf-8')
logger = logging.getLogger("cloudflare_tor_driver")
file_handler = logging.FileHandler("data\\cloudflare_bypass\\logs\\cloudflare_tor_driver.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

try:
    driver = CloudflareTorDriver(logger=logger)
    driver.get_driver("https://pcpartpicker.com/products/cpu/")
    time.sleep(10)
except TimeoutException:
    logger.error(f"TimeoutException ошибка обработана. get_data_from_page")