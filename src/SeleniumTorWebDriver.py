import logging
from logging import Logger
import time
from typing import List

import undetected_chromedriver as uc

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver

from src.SeleniumWebDriver import SeleniumWebDriver
from src.TorManager import TorManager
from src.TorUserData import TorUserData

START_PORT = 8000
END_PORT = 9149
PORTS_COUNT_TO_RESTART = 100

class SeleniumTorWebDriver:
    def __init__(self, 
                 logger: Logger = None, 
                 start_port = START_PORT, 
                 end_port = END_PORT, 
                 ports_count_to_restart = PORTS_COUNT_TO_RESTART):
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

    # метод для удаления Tor порта
    # при кол-во портов < PORTS_COUNT_TO_RESTART, происходит перезапуск Tor
    def remove_port(self, port: int):
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

    def clear_web_drivers(self, web_driver: WebDriver):
        web_driver.close()
        web_driver.quit()

        if self.current_port != None:
            self.remove_port(self.current_port)

    def get_driver(self,
                   is_images_load: bool = True,
                   headless: bool = False):
        driver = None
        user_data = None
        while True:
            try:
                user_data: TorUserData = TorManager.get_random_user(self.users_data)
                self.current_port = user_data.port

                chrome_options = uc.ChromeOptions()
                chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:' + str(user_data.port))

                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_argument("--disable-features=CSSGridLayout")
                chrome_options.add_argument("--blink-settings=imagesEnabled=false")

                #chrome_options.add_argument("--incognito")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-software-rasterizer")
                chrome_options.add_argument("--disable-default-apps")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--disable-infobars")
                chrome_options.add_argument("--disable-ipc-flooding-protection")
                chrome_options.add_argument("--disable-renderer-backgrounding")
                chrome_options.add_argument("--enable-features=NetworkService")
                chrome_options.add_argument("--force-color-profile=srgb")
                chrome_options.add_argument("--hide-scrollbars")
                chrome_options.add_argument("--ignore-certificate-errors")
                chrome_options.add_argument("--log-level=0")
                chrome_options.add_argument("--metrics-recording-only")
                chrome_options.add_argument("--mute-audio")

                if headless == True:
                    chrome_options.add_argument('--headless') 

                if is_images_load == False:
                    prefs = {"profile.managed_default_content_settings.images": 2,
                             "profile.default_content_setting_values.notifications": 2}
                    chrome_options.add_experimental_option("prefs", prefs)

                driver = uc.Chrome(enable_cdp_events=True, options=chrome_options)
                disable_css_script = """
                var style = document.createElement('style');
                style.type = 'text/css';
                style.innerText = 'body { visibility: hidden !important; }';
                document.head.appendChild(style);
                """
                driver.execute_script(disable_css_script)
                return driver
            except selenium.common.exceptions.WebDriverException as e:
                self.logger.error(f"Ошибка WebDriverException обработана.")
                self.remove_port(self.current_port)
                continue