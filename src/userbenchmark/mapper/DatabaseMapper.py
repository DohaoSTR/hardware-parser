import json
import os
import time

import logging
from logging import Logger
import sys
import traceback

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from .API import API
from ..Part import Part

from .db_entities.PartEntity import PartEntity
from .db_entities.PartsKey import PartsKey
from .db_entities.PartsCompareKey import PartsCompareKey
from .db_entities.Metric import Metric
from .db_entities.FPSData import FPSData
from .db_entities.Games import Games

HOST = "localhost"
USER_NAME = "root"
PASSWORD = "root"
DATABASE_NAME = "userbenchmark_data"

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
    
    def add_parts(self):
        try:
            parts = API.get_resources()

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
            game_keys = API.get_game_keys_entities()

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
            keys_items = API.get_keys_of_all_parts()

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
            keys_items = API.get_compare_keys_of_all_parts()

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
            metric_items = API.get_metrics_of_all_parts()

            for item in metric_items:
                key = item["Key"]
                gaming = item["Gaming"]
                desktop = item["Desktop"]
                workstation = item["Workstation"]

                parts_key = self.session.query(PartsKey).filter_by(key=key).first()
                part = self.session.query(PartEntity).filter_by(id = parts_key.id).first()

                #if self.session.query(Metric).filter_by(part=part).count() < 1:
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

    def add_part_metrics_data(self, part: Part):
        try:
            data = API.get_data_of_part(part)

            for entity in data:
                key_entity = self.session.query(PartsCompareKey).filter_by(key=entity.key).first()
                part = self.session.query(PartEntity).filter_by(id = key_entity.id).first()
                
                metrics = entity.metrics
                metrics.part = part

                user_data = entity.user_data
                user_data.part = part

                self.session.add(metrics)
                self.session.add(user_data)

            self.session.commit()
            return True
        except Exception as e:
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

            self.logger.error(f"Класс UserBenchmarkToDBMapper. Метод add_cpu_data. Ошибка - {str(e)}")
            return False

    def add_all_parts(self):
        for part in Part:
            self.add_part_metrics_data(part)
    
    def add_unadded_fps_data(self):
        try:
            start_time = time.time()
            fps_data = API.get_all_fps_data()

            index = 0
            errors_items = []
            for item in fps_data:
                index += 1

                if index % 1000 == 0:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    print(f"{index}; Время: 1000 записей за {execution_time} секунд.")

                if item["samples_value"] == None and item["fps_value"] == None:
                    pass
                else:
                    cpu_key = item["cpu_key"]
                    gpu_key = item["gpu_key"]

                    cpu_key_entity = None
                    gpu_key_entity = None

                    if cpu_key != 0:
                        cpu_key_entity = self.session.query(PartsKey).filter_by(key=cpu_key).first()

                    if gpu_key != 0:
                        gpu_key_entity = self.session.query(PartsKey).filter_by(key=gpu_key).first()
                    
                    cpu = None
                    if cpu_key_entity != None:
                        cpu = self.session.query(PartEntity).filter_by(id = cpu_key_entity.part_id).first()

                    gpu = None
                    if gpu_key_entity != None:
                        gpu = self.session.query(PartEntity).filter_by(id = gpu_key_entity.part_id).first()

                    if cpu != None or gpu != None:
                        game = self.session.query(Games).filter_by(key = int(item["game_key"])).first()
                        
                        entity = FPSData(fps = item["fps_value"],                                   
                                         samples = item["samples_value"],
                                         resolution = item["resolution"], 
                                         game_settings = item["game_settings"],
                                         cpu = cpu,
                                         gpu = gpu,
                                         game = game)
                        
                        fps_item = self.session.query(FPSData).filter(
                            and_(
                                FPSData.cpu == cpu,
                                FPSData.gpu == gpu,
                                FPSData.game == game,
                                FPSData.resolution == item["resolution"],
                                FPSData.game_settings == item["game_settings"]
                            )
                        ).first()

                        if fps_item is None:
                            self.session.add(entity)
                        else:
                            errors_items.append({ "item": item, 
                                                 "cpu": cpu.id, 
                                                 "gpu": gpu.id })

            current_directory = os.getcwd()
            file_path = current_directory + "\\data\\userbenchmark\\errors_items.json"
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(errors_items, json_file, indent=4)

            self.session.commit()
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Метод выполнился за {execution_time} секунд.")
            return True
        except Exception as e:
            self.logger.error(f"Класс UserBenchmarkToDBMapper. Метод add_unadded_data. Ошибка - {str(e)}")
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