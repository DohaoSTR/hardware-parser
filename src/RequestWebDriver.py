from .misc import is_host_reachable

import logging
from logging import Logger

from urllib.parse import urlparse
import requests

GET_RESPONSE_MAX_ITERATION = 15

HOST_IS_REACHABLE_TIMEOUT = 10
HOST_IS_REACHABLE_PORT = 443

RESPONSE_TIMEOUT = 15

class RequestWebDriver:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def get_response(self, link, headers = None, cookies = None, max_iteration = GET_RESPONSE_MAX_ITERATION):
        current_iteration = 0

        while max_iteration > current_iteration:
            # проверка на доступность хоста
            parsed_url = urlparse(link)
            host = parsed_url.netloc
            if not is_host_reachable(host, HOST_IS_REACHABLE_PORT, timeout=HOST_IS_REACHABLE_TIMEOUT):
                current_iteration = current_iteration + 1
                if current_iteration >= max_iteration:
                    self.logger.warning(f"Достигнуто максимальное количество итераций {max_iteration}. Выполняем действия после {max_iteration} итераций. Link: {link}") if self.logger is not None else None
                    current_iteration = 0
                    continue

                self.logger.warning(f"Хост не доступен. Host: {host}, Link: {link}")     
                continue

            try:
                response = requests.get(link, timeout=RESPONSE_TIMEOUT, headers = headers, cookies = cookies)
            except requests.exceptions.ConnectionError as e:
                self.logger.error(f"Ошибка - requests.exceptions.ConnectionError- обработано, Link: {link}")
                response = None
            except requests.exceptions.ChunkedEncodingError as e:
                self.logger.error(f"Ошибка - requests.exceptions.ChunkedEncodingError - обработано, Link: {link}")
                response = None
            except requests.exceptions.Timeout:
                self.logger.error(f"Ошибка - requests.exceptions.Timeout- обработано, Link: {link}")
                response = None
            
            # Если сервер вернул нулевой ответ, get response может вернуть None, 
            # если возникла ошибка requests.exceptions.ConnectionError или ChunkedEncodingError
            if response is None:
                current_iteration = current_iteration + 1
                if current_iteration >= max_iteration:
                    self.logger.warning(f"Достигнуто максимальное количество итераций {max_iteration}. Выполняем действия после {max_iteration} итераций. Link: {link}")
                    current_iteration = 0
                    continue

                continue      

            # если страница вернула ошибку
            if (response.status_code != 200):
                if (response.status_code == 404):
                    self.logger.info(f"Страница вернула код - 404, Link: {link}")
                    return None
                else:
                    current_iteration = current_iteration + 1
                    if current_iteration >= max_iteration:
                        self.logger.warning(f"Достигнуто максимальное количество итераций {max_iteration}. Выполняем действия после {max_iteration} итераций. Link: {link}")
                        current_iteration = 0
                        continue
                        
                    self.logger.warning(f"Страница вернула ошибку: {response.status_code}, Link: {link}")
                    continue
        
            return response