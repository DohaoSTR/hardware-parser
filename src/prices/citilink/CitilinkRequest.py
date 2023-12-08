import logging
import re

from bs4 import BeautifulSoup

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

from RequestTorWebDriver import RequestTorWebDriver
from TorWebDriver import TorWebDriver

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("userbenchmark_request")
file_handler = logging.FileHandler("userbenchmark_parser\\logs\\userbenchmark_request.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# класс для получения html content с сайта UserBenchmark
class CitilinkRequest:
    def __init__(self, is_multi_threading = False):
        web_driver = RequestTorWebDriver()
        self.web_driver = web_driver

        self.is_multi_threading = is_multi_threading

    # реакция при окончании работы или возникновение ошибки
    def __exit__(self, exc_type, exc_value, traceback):
        logger.info(f"Работа парсера завершена, Link: {self.link}")

        logger.info("Параметры метода __exit__:")
        logger.info(f"Тип возникшего исключения: {exc_type}")
        logger.info(f"Значение исключения: {exc_value}")
        logger.info(f"Объект traceback: {traceback}")

        # если UserBecnhmarkRequest, используется без помощи потоков
        # то закрываем Tor внутри класса
        if self.is_multi_threading == False:
            TorWebDriver.close_tor()

        logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    # метод для получения html content
    def get_html_content(self, link, remove_port_method = None, max_iteration=5):
        current_iteration = 0

        while max_iteration > current_iteration:
            response, port = self.web_driver.get_response(link)

            if response == None: 
                return None
            
            html_content = response.text
            return html_content

        logger.info(f"Не удалось получить результат, Link: {link}")
        return None