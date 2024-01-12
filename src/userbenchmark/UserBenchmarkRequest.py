from ..RequestTorWebDriver import RequestTorWebDriver
from ..TorManager import TorManager

import logging
from logging import Logger

from bs4 import BeautifulSoup

STANDARD_USERBENCHMARK_COOKIES = {
    '1P_JAR': '2023-09-12-10',
    'DSID': 'AGnTgWfxUPixqwpVLMnlFCSAM600O8ix4-V6uohgBwVXPeu71kcIJOwlblyNOIgmBsX_e-XUe99ijQxVkA9yqreM1e1wKUciuExRjNLhoU-2n5A1OMf8pSal7MEsSK_uA-MU16-ApAA6yD4LZjX2KnNFKrhf5oum36ZYFEn1AG5C7IW3yhPwWjxm0jMaRD2b9zMldhavPDecOzcLQ8HkqFsb1em-zvxa194yEaPB9qZNigvDPye0MFis8sGPILzwIEY8UuI9v9iZXaNBmxXsNLEFaMnVPema9zuUUQSXc-MkCCrxnERzswg',
    'IDE': 'AHWqTUnClwDIP7e389ji6jWmC5MPzHxVBwg6Z8kcNepmJGvzVlB_vw5ku1nGp7lSn5M',
    'JSESSIONID': '46166E4DA14A0C0C44EAB205E571A933',
    '_ga': 'GA1.2.879826949.1695068906',
    '_ga_MLL787B5V6': 'GS1.1.1695162400.8.1.1695166209.0.0.0',
    '_gid': 'GA1.2.992091052.1695068906',
    'ar_debug': '1',
    'rememberMe': 'iPO2YghVt7MGfIVrLIZ3JfL7fsMYAo2NCNwUqpCTm0a3jAcoQ/Fm63TtYgL14rnOVHNYxfTBBPGnQF/WQECkZuJSbM/vQj3WRQ9ZmdDLPkNQSc3yISsnOm3kgir9omgDFb1ZBLU0uE7mprADmSOAMMBjVlAxJX2B5Qc5oaW1cX1GYSrjkcAh//0ghXaB4dW55b/hM2VFRLNyM48LetU6orUZuLdT426b59f7tqSXFH/Wq/+m9e0TVwAoacVjryEWnJE1x5irFmIE8mIkPaaoGxc21ADbiD702HXZKXLSfdiKH+vEQKdoJSGy3YwZJ8H5E5p6JqsioWGOegQJm64A5ojt0Ze7tmUdGIgER5wb0ZNAD1GWWbsUXkcERjTXI2kJHEo4tQNeSiCP4kLYGYvfkBDPbTlKUHMl2Y5TNA0nPSZQ0uVLQTzeSDJjeJ1gI6AAQ2/wjcN7RAy1IRjQ4utPc4MNiED2NPc+gCexIFjbCzatWKv7HstS09jt3ekb71cL',
}

HTML_CONTENT_MAX_ITERATION = 5

# класс для получения html content с сайта UserBenchmark
class UserBecnhmarkRequest:
    def __init__(self, logger: Logger = None, is_multi_threading = False):
        self.logger = logger or logging.getLogger(__name__)

        web_driver = RequestTorWebDriver(logger)
        self.web_driver = web_driver

        self.tor_manager = TorManager(logger)

        self.is_multi_threading = is_multi_threading

    # реакция при окончании работы или возникновение ошибки
    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info(f"Работа парсера завершена, Link: {self.link}")

        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")

        # если UserBecnhmarkRequest, используется без помощи потоков
        # то закрываем Tor внутри класса
        if self.is_multi_threading == False:
            self.tor_manager.close_tor()

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    def set_async(self, async_parser):
        self.async_parser = async_parser

    # метод для удаления порта
    # останавливает все потоки для удаления порта
    def __remove_port(self, port):
        with self.async_parser.lock:
            if self.async_parser:
                return self.web_driver.remove_port(port)
            else:
                return False

    # метод для получения html content
    def get_html_content(self, link, max_iteration = HTML_CONTENT_MAX_ITERATION):
        current_iteration = 0

        while max_iteration > current_iteration:
            response, port = self.web_driver.get_response(link, cookies=STANDARD_USERBENCHMARK_COOKIES)

            if (response.status_code != 200):
                if (response.status_code == 410):
                    self.logger.info(f"Страница вернула код - 410, Link: {link}")
                    response = None
                else:
                    self.logger.warning(f"Страница вернула ошибку: {response.status_code}, Link: {link}")

                    if self.is_multi_threading == True:
                        self.__remove_port(port)
                    else:
                        self.web_driver.remove_port(port)

                    continue

            if response == None:
                self.logger.info(f"Response равен None, get_html_content. Link: {link}")
                return None
            
            html_content = response.text

            # попали на автообновляемую страницу - значит game_key не существует
            if 'http-equiv="Refresh"' in html_content:
                self.logger.info(f"Автообновляемая страница - refresh, Link: {link}")
                return None
            else:
                try:             
                    soup = BeautifulSoup(html_content, 'html.parser')
                    paragraphs = soup.find_all('p')

                    # ip адрес ограничили из-за большого кол-ва запросов
                    if len(paragraphs) == 0 or not paragraphs:
                        messages = soup.find_all('li', string=[
                        'Excessive requests per second (please login).',
                        'Extensions triggering background page requests (e.g. Ghostery).',
                        'Cookies disabled (3rd party not required).'
                        ])
                        if messages:
                            self.logger.info(f"Много запросов с одного IP. Link: {link}, Port: {port}")
                        else:
                            self.logger.info(f"Paragraphs нету на странице, но в messages другие сообщения, Link: {link}")
                        
                        if self.is_multi_threading == True:
                            self.__remove_port(port)
                        else:
                            self.web_driver.remove_port(port)
                                
                        continue
                    
                    # ip адрес заблокировали
                    if paragraphs and len(paragraphs) > 0:
                        if "blacklisted with activity code (19)" in paragraphs[0].text:
                            self.logger.info(f"IP-адрес находится в черном списке с кодом активности 19. Link: {link}, Port: {port}")
                            current_iteration = 0

                            if self.is_multi_threading == True:
                                self.__remove_port(port)
                            else:
                                self.web_driver.remove_port(port)

                            continue

                    return html_content
                except Exception as e:
                    self.logger.error(f"Произошла ошибка в get_html_content: {str(e)}.")
                    continue

        self.logger.error(f"Не удалось получить результат, Link: {link}")
        return None
    
    def get_image_response(self, link, max_iteration = HTML_CONTENT_MAX_ITERATION):
        current_iteration = 0

        while max_iteration > current_iteration:
            response, port = self.web_driver.get_response(link, cookies=STANDARD_USERBENCHMARK_COOKIES)

            if (response.status_code != 200):
                if (response.status_code == 410):
                    self.logger.info(f"Страница вернула код - 410, Link: {link}")
                    response = None
                else:
                    self.logger.warning(f"Страница вернула ошибку: {response.status_code}, Link: {link}")

                    if self.is_multi_threading == True:
                        self.__remove_port(port)
                    else:
                        self.web_driver.remove_port(port)

                    continue

            if response == None:
                self.logger.info(f"Response равен None, get_html_content. Link: {link}")
                return None
            
            return response

        self.logger.error(f"Не удалось получить результат, Link: {link}")
        return None