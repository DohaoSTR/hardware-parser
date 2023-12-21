import os
from .misc import close_process
from .config_manager import config

from logging import Logger
import logging

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service

STANDARD_USER_AGENT = config.get("SeleniumSettings", "STANDARD_USER_AGENT")

CHROME_PROCESS_NAME = config.get("SeleniumSettings", "CHROME_PROCESS_NAME")
PAUSE_SECONDS_BEFORE_CLOSE_CHROME = config.getint("SeleniumSettings", "PAUSE_SECONDS_BEFORE_CLOSE_CHROME")
PAUSE_SECONDS_AFTER_CLOSE_CHROME = config.getint("SeleniumSettings", "PAUSE_SECONDS_AFTER_CLOSE_CHROME")

CHROME_DRIVER_RELATIVE_PATH = config.get("SeleniumSettings", "CHROME_DRIVER_RELATIVE_PATH")
CHROME_BROWSER_RELATIVE_PATH = config.get("SeleniumSettings", "CHROME_BROWSER_RELATIVE_PATH")

class SeleniumWebDriver:
    def __init__(
        self, 
        logger: Logger = None
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)

    def get_web_driver(
        self,
        port: int = None, 
        user_agent: str = STANDARD_USER_AGENT, 
        headless: bool = False, 
        download_directory: str = None,
        is_images_load: bool = False
    ) -> WebDriver:
        chrome_options = webdriver.ChromeOptions()

        if headless == True:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("ignore-certificate-errors")
        chrome_options.add_argument("--ignore-certificate-errors-spki-list")

        if is_images_load == True:
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)

        chrome_options.add_argument('log-level=3')

        if download_directory != None and len(download_directory) != 0:
            prefs = {"download.default_directory": download_directory}
            chrome_options.add_experimental_option("prefs", prefs)

        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        if port != None:
            chrome_options.add_argument("proxy-server=socks5://127.0.0.1:" + str(port))

        chrome_options.add_argument(f"user-agent={user_agent}")

        current_directory = os.getcwd()
        chrome_driver_exe_path = current_directory + CHROME_DRIVER_RELATIVE_PATH
        service = Service(executable_path=chrome_driver_exe_path)

        chrome_browser_path = current_directory + CHROME_BROWSER_RELATIVE_PATH
        chrome_options.binary_location = chrome_browser_path

        web_driver = webdriver.Chrome(options=chrome_options, service=service)
        web_driver.maximize_window()
        stealth(web_driver,
                languages=["en-US"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
           )

        web_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        web_driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            const newProto = navigator.__proto__
            delete newProto.webdriver
            navigator.__proto__ = newProto
            """
            })
        
        return web_driver
    
    # метод для закрытия всех webdriver-ов
    def close_all_drivers(
        self, 
        pause_seconds_before_close: int = PAUSE_SECONDS_BEFORE_CLOSE_CHROME, 
        pause_seconds_after_close: int = PAUSE_SECONDS_AFTER_CLOSE_CHROME, 
    ) -> bool:
        return close_process(pause_seconds_before_close, pause_seconds_after_close,  CHROME_PROCESS_NAME, self.logger)

    def clear_web_drivers(
        self, 
        web_driver: WebDriver,
        close_all_drivers: bool = True
    ) -> bool:
        if web_driver != None:
            web_driver.delete_all_cookies()
            web_driver.quit()
        else:
            self.logger.warning(f"Web driver равен None. "
                                "SeleniumWebDriver.clear_web_drivers")
            
        if close_all_drivers == True:
            return self.close_all_drivers()
        else:
            return True