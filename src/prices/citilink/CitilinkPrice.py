import logging
import sys
import os
import threading

from bs4 import BeautifulSoup


project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

from CitilinkRequest import CitilinkRequest
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

#https://www.citilink.ru/catalog/processory/

class CitilinkPrice:
    def __init__(self):
        self.lock = threading.Lock()

        web_driver = CitilinkRequest(is_multi_threading=True)
        self.web_driver = web_driver

        self.link = None
        self.fps_data = None

    # реакция при окончании работы или возникновение ошибки
    def __exit__(self, exc_type, exc_value, traceback):
        if self.link != None:
            logger.info(f"Работа парсера завершена, Link: {self.link}")

        logger.info("Параметры метода __exit__:")
        logger.info(f"Тип возникшего исключения: {exc_type}")
        logger.info(f"Значение исключения: {exc_value}")
        logger.info(f"Объект traceback: {traceback}")

        #with self.lock:
            #TorWebDriver.close_tor()

        logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self

    # метод для удаления порта
    # останавливает все потоки для удаления порта
    def __remove_port(self, port):
        with self.lock:
            self.web_driver.remove_port(port)

    # метод для получения данных о городе на странице
    def __get_city_of_page(self, html):
        pass

    # метод для получения всех комплектующих со страницы
    # в формате { name, price, link, product_code, city }
    def get_page_data(self, link):
        self.link = link
        html_content = self.web_driver.get_html_content(link, remove_port_method=self.__remove_port)
            
        soup = BeautifulSoup(html_content, 'html.parser')

        product_snippets = soup.find_all('div', class_="e12wdlvo0")
        print(product_snippets[3])


if __name__ == "__main__":
    parser = CitilinkPrice()
    with parser:
        parser.get_page_data("https://www.citilink.ru/catalog/processory/")
        


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