import logging
from .misc import is_host_reachable
from .PlanetVPNManager import PlanetVPNManager

from logging import Logger

from urllib.parse import urlparse
import requests

STANDARD_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

class RequestPlanetVPNWebDriver:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        
        self.planet_vpn_manager = PlanetVPNManager(logger)
        self.planet_vpn_manager.restart()

    def __exit__(self, exc_type, exc_value, traceback):
        self.planet_vpn_manager.close()

        self.logger.info(f"Работа RequestPlanetVPNDriver завершена")

        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}") 
        self.logger.info(f"Объект traceback: {traceback}")
        
        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    def close(self):
        self.planet_vpn_manager.close()

    def start(self):
        self.planet_vpn_manager.start()

    def restart(self):
        self.planet_vpn_manager.restart()

    def get_response(self, link, headers = None, cookies = None, max_iteration = 3):
        current_iteration = 0

        while max_iteration > current_iteration:
            # проверка на доступность хоста
            parsed_url = urlparse(link)
            host = parsed_url.netloc
            if not is_host_reachable(host, 443):
                current_iteration = current_iteration + 1
                if current_iteration >= max_iteration:
                    self.logger.warning(f"Достигнуто максимальное количество итераций {max_iteration}. Выполняем действия после {max_iteration} итераций. Link: {link}")
                    current_iteration = 0
                    self.planet_vpn_manager.restart()
                    continue

                self.logger.warning(f"Хост не доступен. Host: {host}, Link: {link}")
                continue

            try:
                response = requests.get(link, timeout=15, headers = headers, cookies = cookies)
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
                    self.planet_vpn_manager.restart()
                    continue

                continue      

            # если страница вернула ошибку
            if (response.status_code != 200):
                if response.status_code == 404:
                    return None
                else:
                    current_iteration = current_iteration + 1
                    if current_iteration >= max_iteration:
                        self.logger.warning(f"Достигнуто максимальное количество итераций {max_iteration}. Выполняем действия после {max_iteration} итераций. Link: {link}")
                        current_iteration = 0
                        self.planet_vpn_manager.restart()
                        continue
                        
                    self.logger.warning(f"Страница вернула ошибку: {response.status_code}, Link: {link}")
                    continue
        
            return response