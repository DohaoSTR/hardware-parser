import logging
from logging import Logger
import re
import sys
import traceback

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from src.prices.citilink.db_mapper.Product import Product
from src.prices.citilink.db_mapper.Price import Price

HOST = "a0871451.xsph.ru"
USER_NAME = "a0871451_prices"
PASSWORD = "R2AXjG009yl4Ic6nxNAW"
DATABASE_NAME = "a0871451_prices"

class DatabaseMapper:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        self.engine = create_engine(f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}?charset=utf8mb4")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")

        if self.session == None:
            self.session.close()
        else:
            self.logger.warning("DatabaseMapper, __exit__ - session равен None.")

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self

    def add_products_data(self, products_data):
        try:
            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for index, item in products_data.items():
                title = item["title"]
                link = item["link"]
                category = item["category"]
                
                part_number = None
                match = re.search(r'\[([^]]+)\]', title)
                if match:
                    part_number = str(match.group(1))

                product = self.session.query(Product).filter_by(link = link).first()
                if product == None:
                    entity = Product(name = title, 
                                     link = link, 
                                     part_number = part_number,
                                     category = category)
                    self.session.add(entity)
            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс DatabaseMapper. Метод add_products_data. Ошибка - {str(e)}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            file_name = exc_traceback.tb_frame.f_globals['__file__']
            line_number = exc_traceback.tb_lineno
            traceback_details = {
                'filename': file_name,
                'lineno': line_number,
                'name': exc_traceback.tb_frame.f_code.co_name,
                'type': exc_type.__name__,
                'message': str(exc_value),
                'traceback': traceback.format_exc()
            }
            print(f"Ошибка в файле {file_name}, строка {line_number}: {e}")
            print("Подробности ошибки:")
            for key, value in traceback_details.items():
                print(f"{key}: {value}")
            return False
        
    def add_price_data(self, products_data):
        try:
            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for index, item in products_data.items():
                price = item["price"]
                date_time = item["date_time"]
                link = item["link"]

                product = self.session.query(Product).filter_by(link = link).first()
                if product == None:
                    entity = Price(price = price, 
                                   date_time = date_time)
                    entity.product = product

                    self.session.add(entity)
            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс DatabaseMapper. Метод add_price_data. Ошибка - {str(e)}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            file_name = exc_traceback.tb_frame.f_globals['__file__']
            line_number = exc_traceback.tb_lineno
            traceback_details = {
                'filename': file_name,
                'lineno': line_number,
                'name': exc_traceback.tb_frame.f_code.co_name,
                'type': exc_type.__name__,
                'message': str(exc_value),
                'traceback': traceback.format_exc()
            }
            print(f"Ошибка в файле {file_name}, строка {line_number}: {e}")
            print("Подробности ошибки:")
            for key, value in traceback_details.items():
                print(f"{key}: {value}")
            return False
    
    ###
    def add_available_data(self, products_data):
        pass