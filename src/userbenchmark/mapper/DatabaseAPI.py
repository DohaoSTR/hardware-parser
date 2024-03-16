import logging
from logging import Logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from src.userbenchmark.mapper.db_entities.PartEntity import PartEntity

from ...config_manager import config

HOST = config.get("LocalHostDB", "HOST")
USER_NAME = config.get("LocalHostDB", "USER_NAME")
PASSWORD = config.get("LocalHostDB", "PASSWORD")
DATABASE_NAME = config.get("LocalHostDB", "USERBENCHMARK_DATABASE_NAME")

class DatabaseAPI:
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
            self.logger.warning("DatabaseAPI, __exit__ - session равен None.")

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    def get_parts(self):
        Base = declarative_base()
        Base.metadata.create_all(self.engine)

        entities = self.session.query(PartEntity).all()

        return entities