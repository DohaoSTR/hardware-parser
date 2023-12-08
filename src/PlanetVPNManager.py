import logging
from .Misc import get_ip_info

from logging import Logger

import os
import subprocess
import time
import psutil

PLANET_VPN_RELATIVE_PATH = "\\external_tools\\PlanetVPN\\PlanetVPN.exe"

class PlanetVPNManager:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def __check_connection(self):
        self.current_ip_address, country = get_ip_info(self.logger)

        if self.current_ip_address == None or country == None:
            return False

        if country == "RU":
            return False
        else:
            return True

    def start(self):
        while True:
            if (self.__check_connection() == True):
                return True
            
            current_directory = os.getcwd()
            file_exe_path = current_directory + PLANET_VPN_RELATIVE_PATH
            
            command = [file_exe_path]

            try:
                subprocess.Popen(command)

                retries = 0
                max_retries = 20
                while retries < max_retries:
                    time.sleep(2)
                    if self.__check_connection():
                        return True
                    else:
                        retries = retries + 1
                        if retries >= max_retries:
                            continue
                continue
            except Exception as e:
                self.logger.error(f"Ошибка при запуске PlanetVPN: {e}")
                return False
    
    def close(self):
        try:
            process_name = "PlanetVPN.exe"
            for process in psutil.process_iter(attrs=['name']):
                    if process.info['name'] == process_name:
                        try:
                            process.terminate()
                        except psutil.NoSuchProcess:
                            pass

            process_name = "openvpn.exe"
            for process in psutil.process_iter(attrs=['name']):
                    if process.info['name'] == process_name:
                        try:
                            process.terminate()
                        except psutil.NoSuchProcess:
                            pass

            time.sleep(2)
            self.logger.info("Процесс PlanetVPN был успешно завершен.")
        except subprocess.CalledProcessError:
            self.logger.error("Не удалось завершить процесс PlanetVPN.")

    def restart(self):
        self.close()
        self.start()