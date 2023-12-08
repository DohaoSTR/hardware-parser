import logging
from logging import Logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from .UserBenchmarkAPI import UserBenchmarkAPI
from userbenchmark.UserBenchmarkResources import UserBenchmarkResources

HOST = "localhost"
USER_NAME = "root"
PASSWORD = "root"
DATABASE_NAME = "userbenchmark_data"

class UserBenchmarkToDBMapper:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        self.engine = create_engine(f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}")
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
    
    def add_all_resources(self):
        try:
            parts_entities = UserBenchmarkResources.g()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)
    
            for part_entity in parts_entities:
                self.session.add(part_entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_parts_data. Ошибка - {str(e)}")
            return False
        
    def add_all_cpu(self):
        pass

    def add_all_gpu(self):
        pass

    def add_all_ssd(self):
        pass

    def add_all_hdd(self):
        pass

    def add_all_ram(self):
        pass