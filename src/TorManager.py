from .TorUserData import TorUserData
from .config_manager import config
from .misc import close_process

from logging import Logger
import logging

from typing import List

import subprocess
import os
import random
import requests

STANDARD_USER_AGENT = config.get("SeleniumSettings", "STANDARD_USER_AGENT")

STANDARD_PORT = config.getint("TorSettings", "STANDARD_PORT")
START_PORT = config.getint("TorSettings", "START_PORT")
END_PORT = config.getint("TorSettings", "END_PORT")

TOR_PROCESS_NAME = config.get("TorSettings", "TOR_PROCESS_NAME")
PAUSE_SECONDS_BEFORE_CLOSE_TOR = config.getint("TorSettings", "PAUSE_SECONDS_BEFORE_CLOSE_TOR")
PAUSE_SECONDS_AFTER_CLOSE_TOR = config.getint("TorSettings", "PAUSE_SECONDS_AFTER_CLOSE_TOR")

CHECK_TOR_CONNECTION_RETRIES = config.getint("TorSettings", "CHECK_TOR_CONNECTION_RETRIES")
TOR_RELATIVE_PATH = config.get("TorSettings", "TOR_RELATIVE_PATH")

STANDARD_URL_TO_CHECK_TOR_CONNECTION = config.get("TorSettings", "STANDARD_URL_TO_CHECK_TOR_CONNECTION")
CHECK_TOR_CONNECTION_RESPONSE_TIMEOUT = config.getint("TorSettings", "CHECK_TOR_CONNECTION_RESPONSE_TIMEOUT")

MAX_TOR_RESTART_RETRIES = config.getint("TorSettings", "MAX_TOR_RESTART_RETRIES")

# класс для работы с Tor
class TorManager:
    def __init__(
        self, 
        logger: Logger = None
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def get_users_data(
        startPort: int = START_PORT, 
        endPort: int = END_PORT,
        user_agents: List[str] = None
    ) -> list[TorUserData]:
        if user_agents is None:
            user_agents = [STANDARD_USER_AGENT] * (endPort - startPort)

        users_data = []

        for port, user_agent in zip(range(startPort, endPort), user_agents):
            user_data = TorUserData(port, user_agent)
            users_data.append(user_data)
            
        return users_data
    
    def get_random_user(
        users_data: List[TorUserData] = None
    ) -> TorUserData | None:
        if users_data is None:
            users_data = TorManager.get_users_data()
        
        ports = list(user.port for user in users_data)
        random_port = random.choice(ports)

        if random_port != None and random_port in ports:
            found_user_data = None

            for user_data in users_data:
                if user_data.port == random_port:
                    found_user_data = user_data
                    break

            user_data = TorUserData(random_port, found_user_data.user_agent)
            return user_data
    
        return None

    def get_standard_user_data() -> TorUserData:
        user_data = TorUserData(STANDARD_PORT, STANDARD_USER_AGENT)
        
        return user_data
    
    def close_tor(
        self, 
        pause_seconds_before_close : int = PAUSE_SECONDS_BEFORE_CLOSE_TOR,
        pause_seconds_after_close: int = PAUSE_SECONDS_AFTER_CLOSE_TOR
    ) -> bool:
        return close_process(pause_seconds_before_close, pause_seconds_after_close, TOR_PROCESS_NAME, self.logger)

    def start_tor(
        self, 
        check_tor_connection_retries: int = CHECK_TOR_CONNECTION_RETRIES, 
        tor_relative_path: str = TOR_RELATIVE_PATH,
        close_tor_before_start: bool = True,
        pause_seconds_before_close: int = PAUSE_SECONDS_BEFORE_CLOSE_TOR,
        pause_seconds_after_close: int = PAUSE_SECONDS_AFTER_CLOSE_TOR
    ) -> bool:
        if self.check_tor_connection() == True:
            return True
        
        if close_tor_before_start == True:
            if self.close_tor(pause_seconds_before_close, pause_seconds_after_close) == False:
                return False
        
        current_directory = os.getcwd()
        tor_exe_path = current_directory + tor_relative_path
        command = [tor_exe_path]

        try:
            subprocess.Popen(command)

            retries = 0
            while retries < check_tor_connection_retries:
                if self.check_tor_connection():
                    return True
                else:
                    retries = retries + 1

            return False
        except Exception as e:
            self.logger.error(f"Ошибка при запуске Tor: {e}")
            return False
        
    def check_tor_connection(
        self, 
        port: int = STANDARD_PORT, 
        url: str = STANDARD_URL_TO_CHECK_TOR_CONNECTION, 
        response_timeout: int = CHECK_TOR_CONNECTION_RESPONSE_TIMEOUT
    ) -> bool:
        proxy = {
            "http": f"socks5://127.0.0.1:{port}",
            "https": f"socks5://127.0.0.1:{port}",
        }

        try:
            response = requests.get(
                url, 
                proxies=proxy, 
                timeout=response_timeout
            )
            
            if response.status_code == 200:
                self.logger.info("Tor работает и подключен к сети.")
                return True
            else:
                self.logger.warning("Tor подключен, но возможно есть "
                                    "проблемы с соединением к веб-ресурсу.")
                return False
        except requests.exceptions.RequestException:
            self.logger.error("Произошла ошибка RequestException "
                              "при выполнении запроса через Tor.")
            return False
        except TimeoutError:
            self.logger.error("Произошла ошибка TimeoutError "
                              "при выполнении запроса через Tor.")
            return False
 
    def restart_tor(
        self, 
        max_restart_retries = MAX_TOR_RESTART_RETRIES, 
        check_tor_connection_retries: int = CHECK_TOR_CONNECTION_RETRIES, 
        tor_relative_path: str = TOR_RELATIVE_PATH,
        pause_seconds_after_close: int = PAUSE_SECONDS_AFTER_CLOSE_TOR,
        pause_seconds_before_close: int = PAUSE_SECONDS_BEFORE_CLOSE_TOR
    ) -> bool:
        restart_retries = 0
        while restart_retries < max_restart_retries:
            self.close_tor(pause_seconds_after_close, pause_seconds_before_close)

            close_tor_before_start = False
            is_started = self.start_tor(
                check_tor_connection_retries, 
                tor_relative_path,
                close_tor_before_start,
                pause_seconds_after_close,
                pause_seconds_before_close,
                )

            if is_started == False:
                restart_retries += 1
                continue
            else:
                return True