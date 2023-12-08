import json
import logging
import sys
import os
import time

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)
import undetected_chromedriver as uc

from RequestTorWebDriver import RequestTorWebDriver
from SeleniumWebDriver import SeleniumWebDriver
from TorWebDriver import TorWebDriver

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("citilink")
file_handler = logging.FileHandler("logs\\citilink.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def test():
    port, user = TorWebDriver.get_random_user(TorWebDriver.get_users())

    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:' + str(port))
    web_driver = uc.Chrome(enable_cdp_events=True, options=chrome_options)

    web_driver.get("https://www.dns-shop.ru/product/microdata/d5635852-337e-11eb-a211-00155d03332b/")
    time.sleep(1)
    cookies = web_driver.get_cookies()

    current_file_path = os.path.abspath(__file__)
    save_directory = os.path.dirname(current_file_path) + "\\data\\"

    with open(save_directory + "cookies" + '.json', 'w', encoding='utf-8') as json_file:
        json.dump(cookies, json_file, indent=4, ensure_ascii=False)

    return port

port1 = test()

def test1():
    current_file_path = os.path.abspath(__file__)
    file_path = os.path.dirname(current_file_path) + "\\data\\cookies.json"

    with open(file_path, 'r') as json_file:
        cookies = json.load(json_file)

    cookie_num = {}
    for cookie in cookies:
        cookie_num[cookie['name']] =  cookie['value']

    driver = RequestTorWebDriver()
    response, port = driver.get_response("https://www.dns-shop.ru/product/microdata/d5635852-337e-11eb-a211-00155d03332b/", port=port1)
    print(response.content)

test1()


#https://www.citilink.ru/catalog/processory/?action=changeCity&space=msk_cl 
#https://www.citilink.ru/catalog/processory/?action=changeCity&space=kur_cl%3Akurbryansk
#https://www.citilink.ru/catalog/processory/?action=changeCity&space=spb_cl

# Москва - msk_cl
# Брянск - kur_cl%3Akurbryansk
# Питер - spb_cl

# сделать алгоритм сбора ссылок на смену города через селениум
# сбор ссылок на категории
# сбор

# citilink работает без куков
# nix не работает на request #https://www.nix.ru/price/index.html?gcat_id=2
# dns не работет на request #https://www.dns-shop.ru/?utm_source=www.google.com
# eldorado не работает на request #https://www.eldorado.ru/c/materinskie-platy/

# все что не работает на request необходимо запускать на селениум