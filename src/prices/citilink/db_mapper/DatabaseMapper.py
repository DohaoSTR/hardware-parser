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
from src.prices.citilink.db_mapper.Available import Available

from ....config_manager import config

HOST = config.get("HostDB", "HOST")
USER_NAME = config.get("PricesUser", "USER_NAME")
PASSWORD = config.get("PricesUser", "PASSWORD")
DATABASE_NAME = config.get("HostDB", "USERBENCHMARK_DATABASE_NAME")

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

        if self.session != None:
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
                    part_number = str(match.group(1)).upper()

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
                if product != None:
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
    
    def add_available_data(self, products_data):
        try:
            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for index, item in products_data.items():
                date_time = item["date_time"]
                link = item["link"]

                available = item["available"]
                city_name = item["city_name"]

                product = self.session.query(Product).filter_by(link = link).first()
                if product != None:
                    entity = Available(is_available = available,
                                       city_name = city_name,
                                       date_time = date_time)
                    entity.product = product

                    self.session.add(entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс DatabaseMapper. Метод add_available_data. Ошибка - {str(e)}")
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
        
    def get_most_actual_prices(self):
        sql_query = text(f"call get_most_actual_citilink_prices()")
        result = self.session.execute(sql_query)
        rows = result.fetchall()

        prices = []
        for row in rows:
            dns_price = Price(id=row.id, price=row.price, date_time=row.date_time, product_id=row.product_id)
            prices.append(dns_price)

        return prices
    
    def get_most_actual_available_records(self):
        sql_query = text(f"call get_most_actual_citilink_available()")
        result = self.session.execute(sql_query)
        rows = result.fetchall()

        available_records = []
        for row in rows:
            available_record = Available(id=row.id, 
                                  is_available=row.is_available, 
                                  date_time=row.date_time,
                                  city_name = row.city_name,
                                  product_id=row.product_id)
            available_records.append(available_record)

        return available_records

    def get_products_without_record(self):
        sql_query = text(f"call get_citilink_products_without_record()")
        result = self.session.execute(sql_query)
        rows = result.fetchall()

        products = []
        for row in rows:
            product = Product(id=row.id, 
                                name=row.name, 
                                link=row.link, 
                                part_number=row.part_number,
                                category=row.category)
            products.append(product)

        return products