from src.SeleniumWebDriver import SeleniumWebDriver

import time

import logging
from logging import Logger

LOG_PATH = "data\\logs\\selenium_web_driver_test.log"

def do_sequential_operation_with_selenium(logger: Logger = None):
    selenium = SeleniumWebDriver(logger)
    web_driver = selenium.get_web_driver()

    web_driver.get("https://www.youtube.com/?gl=RU&hl=ru")

    time.sleep(10)

    selenium.clear_web_drivers(web_driver, True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8')
    logger = logging.getLogger("selenium_web_driver")
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    do_sequential_operation_with_selenium(logger)