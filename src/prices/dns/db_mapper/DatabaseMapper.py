import logging
from logging import Logger
import sys
import time
import traceback

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from src.prices.dns.ProductsParser import ProductsParser

from src.prices.dns.db_mapper.Price import Price
from src.prices.dns.db_mapper.Product import Product
from src.prices.dns.db_mapper.Available import Available

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

        if self.session != None:
            self.session.close()
        else:
            self.logger.warning("DatabaseMapper, __exit__ - session равен None.")

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self

    def add_products_data(self, micro_data: dict, products_data):
        try:
            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            data = []
            for index, item in products_data.items():
                uid = item["uid"]
                link = item["link"]
                category = item["category"]

                part_number = None
                for spec in item["specs"]:
                    if spec["Name"] == "Код производителя":
                        part_number = str(spec["Value"]).replace("[", "").replace("]", "").replace("{", "").replace("}", "")
                        if part_number == "нет":
                            part_number == None

                micro_data_item = micro_data.get(index)
                if micro_data_item != None:
                    entity = Product(uid=uid, 
                                    name=micro_data_item["name"], 
                                    part_number=part_number, 
                                    link=link, 
                                    category=category)
                    
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

    def add_prices(self, micro_data):
        try:
            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            data = []
            for index, item in micro_data.items():
                price = item["price"]
                date_time = item["date_time"]
                uid = item["uid"]

                product = self.session.query(Product).filter_by(uid = uid).first()
                entity = Price(price=float(price), 
                                date_time=date_time)
                entity.product = product
                
                self.session.add(entity)
            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс DatabaseMapper. Метод add_prices. Ошибка - {str(e)}")
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

    def add_available_data(self, data):
        try:
            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                status = item["status"]
                city_name = item["city_name"]
                delivery_info = item["delivery_info"]
                date_time = item["date_time"]
                uid = item["uid"]

                product = self.session.query(Product).filter_by(uid = uid).first()

                if product != None:
                    entity = Available(delivery_info = delivery_info, 
                                    status = status,
                                    date_time = date_time,
                                    city_name = city_name)
                    entity.product = product
                else:
                    parser = ProductsParser(self.logger)
                    parser.save_products_to_parse(uid)
                
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
        sql_query = text(f"call get_most_actual_dns_prices()")
        result = self.session.execute(sql_query)
        rows = result.fetchall()

        prices = []
        for row in rows:
            dns_price = Price(id=row.id, price=row.price, date_time=row.date_time, product_id=row.product_id)
            prices.append(dns_price)

        return prices