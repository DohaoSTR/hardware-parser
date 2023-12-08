from src.PlanetVPNManager import PlanetVPNManager

import logging

LOG_PATH = "data\\techpowerup\\logs\\vpn_driver.log"

logging.basicConfig(level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
encoding='utf-8')
logger = logging.getLogger("vpn_driver")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

driver = PlanetVPNManager()
driver.start()
driver.close()