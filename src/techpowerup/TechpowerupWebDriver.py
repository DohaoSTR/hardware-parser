from ..RequestPlanetVPNWebDriver import RequestPlanetVPNWebDriver

import logging
from logging import Logger
from bs4 import BeautifulSoup

HTML_GET_MAX_ITERATION = 3

class TechpowerupWebDriver:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        self.link = None
        self.web_driver = RequestPlanetVPNWebDriver(logger)

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info(f"Работа TechpowerupWebDriver завершена, Link: {self.link}")

        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")

        self.web_driver.close()
        
        self.logger.info("Вызван метод __exit__, ресурсы очищены.")
 
    def __enter__(self):
        return self
    
    def __check_http_status_429(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        http_status = soup.find('h1', string='HTTP 429 - Too Many Requests')

        if http_status:
            return True
        else:
            return False
    
    def __check_not_found(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.find('body').text
        
        if "CPU not found" in text_content or "Card not found" in text_content or "Drive not found" in text_content:
            return True
        else:
            return False
    
    def close(self):
        self.web_driver.close()
        
    def get_html_content(self, link: str, max_iteration: int = HTML_GET_MAX_ITERATION):
        self.link = link
        current_iteration = 0

        while max_iteration > current_iteration:
            response = self.web_driver.get_response(link)

            if response == None:
                return None
            
            html_content = response.text

            if self.__check_http_status_429(html_content) == True:
                current_iteration = current_iteration + 1
                if current_iteration == max_iteration:
                    self.logger.info("Достигнуто максимальное количество итераций (3). Выполняем действия после 3 итераций.")
                    self.web_driver.restart()
                    current_iteration = 0
                    continue

                self.logger.warning(f"Страница вернула статус 429 - Слишком много запросов, Link: {link}")
                continue

            if self.__check_not_found(html_content) == True:
                self.logger.warning(f"Страница пустая, Link: {link}")
                return None

            return html_content