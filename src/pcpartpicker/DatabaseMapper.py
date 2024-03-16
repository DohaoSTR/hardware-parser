import sys
import traceback

from src.pcpartpicker.db_entities.Metric import Metric

from .db_entities.ImageLinkEntity import ImageLinkEntity
from .db_entities.ImageDataEntity import ImageDataEntity
from .db_entities.PartEntity import PartEntity
from .db_entities.PartNumberEntity import PartNumberEntity
from .db_entities.UserRatingEntity import UserRatingEntity
from .db_entities.PriceEntity import PriceEntity

from .db_entities.Compatible.CitilinkCompatible import CitilinkCompatible
from .db_entities.Compatible.DNSCompatible import DNSCompatible
from .db_entities.Compatible.UserBenchmarkCompatible import UserBenchmarkCompatible

from .local_entities.InternalHardDriveEntity import InternalDriveType

from .Part import Part
from .API import API

import logging
from logging import Logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from src.configure.CompatibleMapper import get_dns_pcpartpicker
from src.configure.CompatibleMapper import get_citilink_pcpartpicker
from src.configure.CompatibleMapper import get_pcpartpicker_userbenchmark
from src.configure.CompatibleMapper import get_metrics

from ..config_manager import config

HOST = config.get("HostDB", "HOST")
USER_NAME = config.get("PcPartPickerUser", "USER_NAME")
PASSWORD = config.get("PcPartPickerUser", "PASSWORD")
DATABASE_NAME = config.get("HostDB", "PCPARTPICKER_DATABASE_NAME")

class DatabaseMapper:
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
            self.logger.warning("PcPartPickerToDBMapper, __exit__ - session равен None.")

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self
    
    #
    #
    #
    def add_all_parts_main_data(self):
        try:
            parts_entities = API.get_part_entities_of_all_parts()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)
    
            for part_entity in parts_entities:
                self.session.add(part_entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_parts_data. Ошибка - {str(e)}")
            return False

    def add_all_part_number_data(self):
        try:
            part_number_data = API.get_part_number_data_of_all_parts()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for key, part_number in part_number_data:
                part = self.session.query(PartEntity).filter_by(key=key).first()
                part_number = PartNumberEntity(part_number=part_number, part=part) 
                self.session.add(part_number)
                
            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_part_number_data. Ошибка - {str(e)}")
            return False

    def add_all_user_rating_data(self):
        try:
            user_rating_data = API.get_user_rating_data_of_all_parts()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for key, ratings_count, average_rating, five_star, four_star, three_star, two_star, one_star in user_rating_data:
                part = self.session.query(PartEntity).filter_by(key=key).first()
                
                params = [ratings_count, average_rating, five_star, four_star, three_star, two_star, one_star]
                if all(p is not None for p in params):
                    user_rating = UserRatingEntity(ratings_count=ratings_count, 
                                                   average_rating=average_rating, 
                                                   five_star=five_star, 
                                                   four_star=four_star, 
                                                   three_star=three_star,
                                                   two_star=two_star,
                                                   one_star=one_star, 
                                                   part=part) 
                    self.session.add(user_rating)
            
            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_user_rating_data. Ошибка - {str(e)}")
            return False
        
    def add_all_price_data(self):
        try:
            price_data = API.get_price_data_of_all_parts()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for key, merchant_link, merchant_name, base_price, promo_value, shipping_text, shipping_link, tax_value, availability, final_price, currency, last_update_time in price_data:
                part = self.session.query(PartEntity).filter_by(key=key).first()
                
                params = [merchant_link, merchant_name, base_price, promo_value, shipping_text, shipping_link, tax_value, availability, final_price, last_update_time]
                if any(p is not None for p in params):
                    price_entity = PriceEntity(merchant_link=merchant_link, merchant_name=merchant_name, base_price=base_price, 
                                                              promo_value=promo_value, shipping_text=shipping_text,shipping_link=shipping_link,
                                                              tax_value=tax_value, availability=availability, final_price=final_price, currency=currency,
                                                              last_update_time=last_update_time, part=part) 
                    self.session.add(price_entity)
            
            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_price_data. Ошибка - {str(e)}")
            return False 

    def add_all_image_link_data(self):
        try:
            image_link_data = API.get_image_links_data_of_all_parts()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for key, name, link in image_link_data:
                part = self.session.query(PartEntity).filter_by(key=key).first()
                
                image_link_entity = ImageLinkEntity(name=name, link=link, part=part) 
                self.session.add(image_link_entity)
            
            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_image_link_data. Ошибка - {str(e)}")
            return False

    def add_all_image_data(self):
        try:
            image_data = API.get_image_data()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for key, name, link, bytes in image_data:
                part = self.session.query(PartEntity).filter_by(key=key).first()
                image_link = self.session.query(ImageLinkEntity).filter_by(part_id=part.id).all()

                for item in image_link:
                    if item.name == name:
                        image_data_entity = ImageDataEntity(image_data=bytes, image_link=item) 
                        self.session.add(image_data_entity)
            
            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_image_data. Ошибка - {str(e)}")
            return False
    #
    #
    #


    #
    #
    #
    def add_all_cpu_data(self):
        try:
            data = API.get_specification_data(Part.CPU)

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                part = self.session.query(PartEntity).filter_by(key=item.key).first()

                main_data_entity = item.main_data
                main_data_entity.part = part
                self.session.add(main_data_entity)
                self.session.flush()

                core_entity = item.cpu_core
                core_entity.part = part
                self.session.add(core_entity)

                performance_cache_entity = item.perfomance_cache
                efficiency_cache_entity = item.efficiency_cache
                
                if performance_cache_entity != None:
                    performance_cache_entity.part = part
                    self.session.add(performance_cache_entity)

                if efficiency_cache_entity != None:
                    efficiency_cache_entity.part = part
                    self.session.add(efficiency_cache_entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_cpu_data. Ошибка - {str(e)}")
            return False
    
    def add_all_gpu_data(self):
        try:
            data = API.get_specification_data(Part.VIDEO_CARD)

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                part = self.session.query(PartEntity).filter_by(key=item.key).first()
                
                main_data_entity = item.main_data
                main_data_entity.part = part
                self.session.add(main_data_entity)
                self.session.flush()

                outputs_data = item.outputs_data
                if outputs_data != None:
                    outputs_data.part = part
                    self.session.add(outputs_data)

                connect_data = item.connect_data
                if connect_data != None:
                    connect_data.part = part
                    self.session.add(connect_data)

                external_power_data_1 = item.external_power_data_1
                if external_power_data_1 != None:
                    external_power_data_1.part = part
                    self.session.add(external_power_data_1)

                external_power_data_2 = item.external_power_data_2
                if external_power_data_2 != None:
                    external_power_data_2.part = part
                    self.session.add(external_power_data_2)

                multi_interface_data = item.multi_interface_data
                if multi_interface_data != None:
                    for interface in multi_interface_data:
                        interface.part = part
                        self.session.add(interface)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_gpu_data. Ошибка - {str(e)}")
            return False
    
    def add_all_memory_data(self):
        try:
            data = API.get_specification_data(Part.MEMORY)

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                part = self.session.query(PartEntity).filter_by(key=item.key).first()

                main_data_entity = item.memory_main_data
                main_data_entity.part = part
                self.session.add(main_data_entity)
                self.session.flush()

                memory_characteristics = item.memory_characteristics
                if memory_characteristics != None:
                    memory_characteristics.part = part
                    self.session.add(memory_characteristics)

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

            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_memory_data. Ошибка - {str(e)}")
            return False
    
    def add_all_motherboard_data(self):
        try:
            data = API.get_specification_data(Part.MOTHEBOARD)

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                part = self.session.query(PartEntity).filter_by(key=item.key).first()

                main_data_entity = item.main_data
                main_data_entity.part = part
                self.session.add(main_data_entity)
                self.session.flush()

                connect_data = item.connect_data
                if connect_data != None:
                    connect_data.part = part
                    self.session.add(connect_data)

                socket_entities = item.socket_entities
                if socket_entities != None:
                    for socket_entity in socket_entities:
                        socket_entity.part = part
                        self.session.add(socket_entity)

                ethernet_entities = item.ethernet_entities
                if ethernet_entities != None:
                    for ethernet_entity in ethernet_entities:
                        ethernet_entity.part = part
                        self.session.add(ethernet_entity)

                memory_speed_entites = item.memory_speed_entites
                if memory_speed_entites != None:
                    for memory_speed_entity in memory_speed_entites:
                        memory_speed_entity.part = part
                        self.session.add(memory_speed_entity)

                m2_entities = item.m2_entities
                if m2_entities != None:
                    for m2_entity in m2_entities:
                        m2_entity.part = part
                        self.session.add(m2_entity)

                multi_interface_data = item.interface_entities
                if multi_interface_data != None:
                    for interface in multi_interface_data:
                        interface.part = part
                        self.session.add(interface)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_motherboard_data. Ошибка - {str(e)}")
            return False
    
    def add_all_internal_hard_drive_data(self):
        try:
            data = API.get_specification_data(Part.STORAGE)

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                part = self.session.query(PartEntity).filter_by(key=item.key).first()

                if item.database_type == InternalDriveType.HDD:
                    hdd = item.hdd
                    hdd.part = part
                    self.session.add(hdd)
                    self.session.flush()

                if item.database_type == InternalDriveType.SSD:
                    ssd = item.ssd
                    ssd.part = part
                    self.session.add(ssd)
                    self.session.flush()

                if item.database_type == InternalDriveType.HYBRID:
                    hybrid_storage = item.hybrid_storage
                    hybrid_storage.part = part
                    self.session.add(hybrid_storage)
                    self.session.flush()

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_internal_hard_drive_data. Ошибка - {str(e)}")
            return False

    def add_all_case_data(self):
        try:
            data = API.get_specification_data(Part.CASE)

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                part = self.session.query(PartEntity).filter_by(key=item.key).first()

                case_data = item.case_data
                case_data.part = part
                self.session.add(case_data)
                self.session.flush()

                front_panel_usb_entities = item.front_panel_usb_entities
                if front_panel_usb_entities != None:
                    for entity in front_panel_usb_entities:
                        entity.part = part
                        self.session.add(entity)

                motherboard_form_factor_entities = item.motherboard_form_factor_entities
                if motherboard_form_factor_entities != None:
                    for entity in motherboard_form_factor_entities:
                        entity.part = part
                        self.session.add(entity)

                drive_bays_entities = item.drive_bays_entities
                if drive_bays_entities != None:
                    for entity in drive_bays_entities:
                        entity.part = part
                        self.session.add(entity)

                expansion_slots_entities = item.expansion_slots_entities
                if expansion_slots_entities != None:
                    for entity in expansion_slots_entities:
                        entity.part = part
                        self.session.add(entity)

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
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_case_data. Ошибка - {str(e)}")
            return False
    
    def add_all_case_fan_data(self):
        try:
            data = API.get_specification_data(Part.CASE_FAN)

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                part = self.session.query(PartEntity).filter_by(key=item.key).first()

                case_fan = item.case_fan
                case_fan.part = part
                self.session.add(case_fan)
                self.session.flush()

                case_fan_connector = item.case_fan_connector
                if case_fan_connector != None:
                    for entity in case_fan_connector:
                        entity.part = part
                        self.session.add(entity)

                case_fan_features = item.case_fan_features
                if case_fan_features != None:
                    for entity in case_fan_features:
                        entity.part = part
                        self.session.add(entity)

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

            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_case_fan_data. Ошибка - {str(e)}")
            return False
    
    def add_all_cpu_cooler_data(self):
        try:
            data = API.get_specification_data(Part.CPU_COOLER)

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                part = self.session.query(PartEntity).filter_by(key=item.key).first()

                cooler_data = item.cooler_data
                cooler_data.part = part
                self.session.add(cooler_data)
                self.session.flush()

                cooler_sockets = item.cooler_sockets
                if cooler_sockets != None:
                    for entity in cooler_sockets:
                        entity.part = part
                        self.session.add(entity)

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_cpu_cooler_data. Ошибка - {str(e)}")
            return False
    
    def add_all_power_supply(self):
        try:
            data = API.get_specification_data(Part.POWER_SUPPLY)

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for item in data:
                part = self.session.query(PartEntity).filter_by(key=item.key).first()

                power_supply = item.power_supply
                power_supply.part = part
                self.session.add(power_supply)
                self.session.flush()

                power_supply_connectors = item.power_supply_connectors
                if power_supply_connectors != None:
                    power_supply_connectors.part = part
                    self.session.add(power_supply_connectors)

                power_supply_efficiency = item.power_supply_efficiency
                if power_supply_efficiency != None:
                    for entity in power_supply_efficiency:
                        entity.part = part
                        self.session.add(entity)

                power_supply_outputs = item.power_supply_outputs
                if power_supply_outputs != None:
                    for entity in power_supply_outputs:
                        entity.part = part
                        self.session.add(entity)
                
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

            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_power_supply. Ошибка - {str(e)}")
            return False
    #
    #
    #
    
    def add_all_dns_ppp(self):
        try:
            data = get_dns_pcpartpicker()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for key, item in data.items():
                entity = DNSCompatible(dns_uid = item["dns_id"], pcpartpicker_id = item["ppp_id"])
                self.session.add(entity)
                
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

            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_dns_ppp. Ошибка - {str(e)}")
            return False
        
    def add_all_citilink_ppp(self):
        try:
            data = get_citilink_pcpartpicker()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for key, item in data.items():
                entity = CitilinkCompatible(citilink_id = item["citilink_id"], pcpartpicker_id = item["ppp_id"])
                self.session.add(entity)
                
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

            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_citilink_ppp. Ошибка - {str(e)}")
            return False
        
    def add_all_pcpartpicker_userbenchmark(self):
        try:
            data = get_pcpartpicker_userbenchmark()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for key, item in data.items():
                entity = UserBenchmarkCompatible(userbenchmark_id = item["ub_id"], pcpartpicker_id = item["ppp_id"])
                self.session.add(entity)
                
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

            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_pcpartpicker_userbenchmark. Ошибка - {str(e)}")
            return False
        
    def add_all_metric(self):
        try:
            data = get_metrics()

            Base = declarative_base()
            Base.metadata.create_all(self.engine)

            for key, item in data.items():
                entity = Metric(gaming_percentage = item["gaming_percentage"], 
                                desktop_percentage = item["desktop_percentage"],
                                workstation_percentage = item["workstation_percentage"],
                                part_id = item["ppp_id"])
                self.session.add(entity)
                
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

            self.logger.error(f"Класс PcPartPickerDataBase. Метод add_all_metric. Ошибка - {str(e)}")
            return False