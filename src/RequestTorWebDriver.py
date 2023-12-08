import logging
from typing import List
from src.TorUserData import TorUserData

from src.misc import is_host_reachable
from .TorManager import TorManager

from logging import Logger
from urllib.parse import urlparse
import requests

STANDARD_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

STANDARD_HEADERS = {'User-Agent': STANDARD_USER_AGENT,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'}

START_PORT = 8000
END_PORT = 9149
PORTS_COUNT_TO_RESTART = 100

HOST_IS_REACHABLE_TIMEOUT = 10
HOST_IS_REACHABLE_PORT = 443

RESPONSE_TIMEOUT = 15

GET_RESPONSE_ITERATION_COUNT = 5

class RequestTorWebDriver:
    def __init__(self, logger: Logger = None, start_port = START_PORT, end_port = END_PORT, ports_count_to_restart = PORTS_COUNT_TO_RESTART):
        self.logger = logger or logging.getLogger(__name__)

        self.tor_manager = TorManager(logger)
        while True:
            if self.tor_manager.start_tor() == False:
                continue
            else:
                break

        self.start_port = start_port
        self.end_port = end_port
        self.ports_count_to_restart = ports_count_to_restart

        self.users_data: List[TorUserData] = TorManager.get_users_data(start_port, end_port)
        
    def remove_port(self, port):
        user_data = next((user for user in self.users_data if user.port == port), None)

        if user_data:
            self.users_data.remove(user_data)
            self.logger.info(f"Порт был удалён. Порт: {port}")

            if (len(self.users_data) < PORTS_COUNT_TO_RESTART):
                self.logger.info("Порты кончились.")
                
                self.tor_manager.restart_tor()

                self.users_data = TorManager.get_users_data(self.start_port, self.end_port)
                self.logger.info("Порты обновлены.")
                
            return True
        else:
            self.logger.warning(f"Порт не найден в списке. Port: {port}")
            return False
        
    # используется в основном для userbench
    # если соединения нету он начинает хуйней заниматься, еще и ничего не вернеться, если итерации перевалят
    def get_response(self, link, default_port = None, headers = STANDARD_HEADERS, cookies = None, max_iteration = 5):
        current_iteration = 0
        while max_iteration > current_iteration:
            # проверка на доступность хоста
            parsed_url = urlparse(link)
            host = parsed_url.netloc
            if not is_host_reachable(host, HOST_IS_REACHABLE_PORT, timeout=HOST_IS_REACHABLE_TIMEOUT):
                self.logger.warning(f"Хост не доступен. Host: {host}, Link: {link}")
                continue
            
            if default_port == None:
                tor_user_data = TorManager.get_random_user(self.users_data)
        
            session = requests.session()
            session.proxies = {'http':  'socks5://127.0.0.1:' + str(tor_user_data.port),
                                'https': 'socks5://127.0.0.1:' + str(tor_user_data.port)}
            
            try:
                response = session.get(link, headers=headers, cookies=cookies, timeout=RESPONSE_TIMEOUT)
            except requests.exceptions.ConnectionError:
                self.logger.error(f"Ошибка - requests.exceptions.ConnectionError - обработано, Link: {link}")
                continue
            except requests.exceptions.ChunkedEncodingError:
                self.logger.error(f"Ошибка - requests.exceptions.ChunkedEncodingError - обработано, Link: {link}")
                continue
            except requests.exceptions.Timeout:
                self.logger.error(f"Ошибка - requests.exceptions.Timeout - обработано, Link: {link}")
                continue

            # Если сервер вернул нулевой ответ, get response может вернуть None, 
            # если возникла ошибка requests.exceptions.ConnectionError или ChunkedEncodingError
            if response is None:
                self.logger.info(f"Response равен None, get_response. Link: {link}")
                continue

            return response, tor_user_data.port