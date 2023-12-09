import logging
from logging import Logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from .UserBenchmarkAPI import UserBenchmarkAPI
from ..UserBenchmarkResources import UserBenchmarkResources

from .db_entities.PartEntity import PartEntity
from .db_entities.PartsKey import PartsKey
from .db_entities.PartsCompareKey import PartsCompareKey
from .db_entities.Metric import Metric

HOST = "localhost"
USER_NAME = "root"
PASSWORD = "root"
DATABASE_NAME = "userbenchmark_data"

class UserBenchmarkToDBMapper:
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
            self.logger.warning("UserBenchmarkToDBMapper, __exit__ - session равен None.")

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    # с такой системой получаются дупликаты данных
    # из за того что один и тот же Key соответствует разным видеокартам 
    # (по сути это правда одни и те же видеокарты)
    # надо придумать что с этим сделать
    def add_parts(self):
        try:
            parts = UserBenchmarkAPI.get_resources()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)
    
            for entity in parts:
                self.session.add(entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс UserBenchmarkToDBMapper. Метод add_parts. Ошибка - {str(e)}")
            return False
    
    def add_games(self):
        try:
            game_keys = UserBenchmarkAPI.get_game_keys_entities()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)
    
            for entity in game_keys:
                self.session.add(entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс UserBenchmarkToDBMapper. Метод add_games. Ошибка - {str(e)}")
            return False

    def add_parts_keys(self):
        try:
            keys_items = UserBenchmarkAPI.get_keys_of_all_parts()

            for item in keys_items:
                key = item["Key"]
                model = item["Model"]

                part = self.session.query(PartEntity).filter_by(model=model).first()

                entity = PartsKey(part = part, key = key)
                self.session.add(entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс UserBenchmarkToDBMapper. Метод add_part_keys. Ошибка - {str(e)}")
            return False

    def add_compare_keys(self):
        try:
            keys_items = UserBenchmarkAPI.get_compare_keys_of_all_parts()

            for item in keys_items:
                key = item["Key"]
                model = item["Model"]
                type = item["Type"]

                part = self.session.query(PartEntity).filter_by(model=model).first()

                entity = PartsCompareKey(part = part, key = key, type = type)
                self.session.add(entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс UserBenchmarkToDBMapper. Метод add_part_keys. Ошибка - {str(e)}")
            return False

    def add_metrics(self):
        try:
            metric_items = UserBenchmarkAPI.get_metrics_of_all_parts()

            for item in metric_items:
                key = item["Key"]
                gaming = item["Gaming"]
                desktop = item["Desktop"]
                workstation = item["Workstation"]

                parts_key = self.session.query(PartsKey).filter_by(key=key).first()
                part = self.session.query(PartEntity).filter_by(id = parts_key.id).first()

                entity = Metric(part = part, 
                                gaming_percentage = gaming, 
                                desktop_percentage = desktop, 
                                workstation_percentage = workstation)
                self.session.add(entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс UserBenchmarkToDBMapper. Метод add_metrics. Ошибка - {str(e)}")
            return False

    #
    def add_cpu_data(self):
        pass

    def add_gpu_data(self):
        pass

    def add_ssd_data(self):
        pass

    def add_hdd_data(self):
        pass

    def add_ram_data(self):
        pass
    
    #
    def add_fps_data(self):
        pass