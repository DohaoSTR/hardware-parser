from .IpData import IpData
from .config_manager import config

from logging import Logger
import logging

import socket
import subprocess
import time
import psutil
import requests

STANDARD_HOST_REACHABLE_TIMEOUT = config.get("IpCheckSettings", "STANDARD_HOST_REACHABLE_TIMEOUT")
STANDARD_PORT = config.get("IpCheckSettings", "STANDARD_PORT")

URL_TO_CHECK_IP = config.get("IpCheckSettings", "URL_TO_CHECK_IP")

# метод для проверки доступности хоста
def is_host_reachable(
    host: str, 
    port: int = STANDARD_PORT,
    timeout: int = STANDARD_HOST_REACHABLE_TIMEOUT
) -> bool:
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except (OSError, ConnectionError):
        return False

def custom_float(value: str) -> float | int:
    if "." in value:
        return float(value)
    else:
        return int(value)

# метод для получения текущего ip-адреса
def get_ip_info(
    logger: Logger = None
) -> IpData | None:
    logger = logger or logging.getLogger(__name__)
    while True:
        try:
            response = requests.get(URL_TO_CHECK_IP)
            data = response.json()

            ip_address = data["ip"]
            country = data["country"]

            logger.info(f"IP-адрес: {ip_address}. Страна: {country}")
            ip_data = IpData(ip_address, country)
            return ip_data
        except requests.exceptions.RequestException as e:
            logger.error(f"Произошла ошибка при выполнении запроса: {str(e)}")
            continue
        except KeyError:
            return None
        
def close_process(
    pause_seconds_before_close : int,
    pause_seconds_after_close: int, 
    process_name: str,
    logger: Logger = None
) -> bool:
        logger = logger or logging.getLogger(__name__)

        time.sleep(pause_seconds_before_close)
        try:
            for process in psutil.process_iter(attrs=["name"]):
                if process.info["name"] == process_name:
                    try:
                        process.terminate()
                    except psutil.NoSuchProcess:
                        pass

            time.sleep(pause_seconds_after_close)
            logger.info(f"Процесс {process_name} был успешно завершен.")
            
            return True
        except subprocess.CalledProcessError:
            logger.error(f"Не удалось завершить процесс {process_name}.")
            return False 