from dataclasses import dataclass
from typing import List
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.pcpartpicker.db_entities.Case.CaseData import CaseData
from src.pcpartpicker.db_entities.Case.CaseDriveBay import CaseDriveBay
from src.pcpartpicker.db_entities.Case.CaseExpansionSlot import CaseExpansionSlot
from src.pcpartpicker.db_entities.Case.CaseMotherboardFormFactor import CaseMotherboardFormFactor

from src.pcpartpicker.db_entities.CaseFan.CaseFanConnector import CaseFanConnector
from src.pcpartpicker.db_entities.CaseFan.CaseFanData import CaseFanData

from src.pcpartpicker.db_entities.CPU.CPUCoreEntity import CPUCoreEntity
from src.pcpartpicker.db_entities.CPU.CPUMainDataEntity import CPUMainDataEntity

from src.pcpartpicker.db_entities.Memory.MemoryCharacteristics import MemoryCharacteristics
from src.pcpartpicker.db_entities.Memory.MemoryMainData import MemoryMainData

from src.pcpartpicker.db_entities.Motherboard.MotherboardConnectData import MotherboardConnectData
from src.pcpartpicker.db_entities.Motherboard.MotherboardMainData import MotherboardMainData
from src.pcpartpicker.db_entities.Motherboard.MotherboardMemorySpeed import MotherboardMemorySpeed
from src.pcpartpicker.db_entities.Motherboard.MotherboardSocket import MotherboardSocket
from src.pcpartpicker.db_entities.Motherboard.MotherboardM2Slots import MotherboardM2Slots

from src.pcpartpicker.db_entities.CPUCooler.CPUCoolerData import CPUCoolerData
from src.pcpartpicker.db_entities.CPUCooler.CPUCoolerSocket import CPUCoolerSocket

from src.pcpartpicker.db_entities.GPU.GPUConnectData import GPUConnectData
from src.pcpartpicker.db_entities.GPU.GPUExternalPower import GPUExternalPowerData
from src.pcpartpicker.db_entities.GPU.GPUMainData import GPUMainData

from src.pcpartpicker.db_entities.InternalDrive.HDD import HDD
from src.pcpartpicker.db_entities.InternalDrive.SSD import SSD

from src.pcpartpicker.db_entities.PowerSupply.PowerSupplyConnectors import PowerSupplyConnectors
from src.pcpartpicker.db_entities.PowerSupply.PowerSupplyData import PowerSupplyData
from src.pcpartpicker.db_entities.PowerSupply.PowerSupplyOutput import PowerSupplyOutput

from src.userbenchmark.mapper.DatabaseAPI import DatabaseAPI as UserBenchmarkDatabaseAPI
from src.pcpartpicker.DatabaseAPI import DatabaseAPI as PcPartPickerDatabaseAPI

from src.pcpartpicker.db_entities.PartEntity import PartEntity as PcPartPickerPartEntity
from src.userbenchmark.mapper.db_entities.PartEntity import PartEntity as UserBenchmarkPartEntity
from src.userbenchmark.mapper.db_entities.Metric import Metric

from src.userbenchmark.mapper.db_entities.FPSData import FPSData

from src.pcpartpicker.db_entities.PriceEntity import PriceEntity

from ..config_manager import config

HOST = config.get("LocalHostDB", "HOST")
USER_NAME = config.get("LocalHostDB", "USER_NAME")
PASSWORD = config.get("LocalHostDB", "PASSWORD")
DATABASE_NAME = config.get("LocalHostDB", "CONFIGURE_DATABASE_NAME")

@dataclass
class MainPart:
    gaming_metric: int
    desktop_metric: int
    workstation_metric: int

    rank: int
    benchmark: int
    samples: int

    userbenchmark_id: int
    pcpartpicker_id: int

@dataclass
class CPU(MainPart):
    fps_data: List[FPSData]

@dataclass
class GPU(MainPart):
    fps_data: List[FPSData]

class ConfigureMapper:
    def __init__(self):
        self.pcpartpicker_api = PcPartPickerDatabaseAPI()
        self.userbenchmark_api = UserBenchmarkDatabaseAPI()

    def get_fps_data(self) -> List[FPSData]:
        return self.userbenchmark_api.session(FPSData).all()

    def get_ram_main_parts(self) -> List[MainPart]:
        entities = []
        for ram_tuple in self.get_ram_entities:
            pcpartpicker_id = ram_tuple[0].id
            userbenchmark_id = ram_tuple[1].id
            rank = ram_tuple[1].rank
            benchmark = ram_tuple[1].benchmark
            samples = ram_tuple[1].samples

            metric = self.userbenchmark_api.session.query(Metric).filter(Metric.part_id == userbenchmark_id).first()

            if metric != None:
                entities.append(MainPart(metric.gaming_percentage, 
                                        metric.desktop_percentage, 
                                        metric.workstation_percentage,
                                        rank,
                                        benchmark, 
                                        samples,
                                        userbenchmark_id,
                                        pcpartpicker_id))
        return entities 
    
    def get_ssd_main_parts(self) -> List[MainPart]:
        entities = []
        for ssd_tuple in self.get_ssd_entities:
            pcpartpicker_id = ssd_tuple[0].id
            userbenchmark_id = ssd_tuple[1].id
            rank = ssd_tuple[1].rank
            benchmark = ssd_tuple[1].benchmark
            samples = ssd_tuple[1].samples

            metric = self.userbenchmark_api.session.query(Metric).filter(Metric.part_id == userbenchmark_id).first()

            if metric != None:
                entities.append(MainPart(metric.gaming_percentage, 
                                        metric.desktop_percentage, 
                                        metric.workstation_percentage,
                                        rank,
                                        benchmark, 
                                        samples,
                                        userbenchmark_id,
                                        pcpartpicker_id))
        return entities 
    
    def get_hdd_main_parts(self) -> List[MainPart]:
        entities = []
        for hdd_tuple in self.get_hdd_entities:
            pcpartpicker_id = hdd_tuple[0].id
            userbenchmark_id = hdd_tuple[1].id
            rank = hdd_tuple[1].rank
            benchmark = hdd_tuple[1].benchmark
            samples = hdd_tuple[1].samples

            metric = self.userbenchmark_api.session.query(Metric).filter(Metric.part_id == userbenchmark_id).first()
            
            if metric != None:
                entities.append(MainPart(metric.gaming_percentage, 
                                        metric.desktop_percentage, 
                                        metric.workstation_percentage,
                                        rank,
                                        benchmark, 
                                        samples,
                                        userbenchmark_id,
                                        pcpartpicker_id))
        return entities 
    
    def get_cpu_main_parts(self) -> List[CPU]:
        entities = []
        for cpu_tuple in self.get_cpu_entities:
            pcpartpicker_id = cpu_tuple[0].id
            userbenchmark_id = cpu_tuple[1].id
            rank = cpu_tuple[1].rank
            benchmark = cpu_tuple[1].benchmark
            samples = cpu_tuple[1].samples

            fps_data = self.userbenchmark_api.session.query(FPSData).filter(FPSData.cpu_id == userbenchmark_id).all()

            metric = self.userbenchmark_api.session.query(Metric).filter(Metric.part_id == userbenchmark_id).first()
            if metric != None:
                entities.append(CPU(metric.gaming_percentage, 
                                        metric.desktop_percentage, 
                                        metric.workstation_percentage,
                                        rank,
                                        benchmark, 
                                        samples,
                                        userbenchmark_id,
                                        pcpartpicker_id,
                                        fps_data))
        return entities 
    
    def get_gpu_main_parts(self) -> List[GPU]:
        entities = []
        for gpu_tuple in self.get_gpu_entities:
            pcpartpicker_id = gpu_tuple[0].id
            userbenchmark_id = gpu_tuple[1].id
            rank = gpu_tuple[1].rank
            benchmark = gpu_tuple[1].benchmark
            samples = gpu_tuple[1].samples
            fps_data = self.userbenchmark_api.session.query(FPSData).filter(FPSData.gpu_id == userbenchmark_id).all()

            metric = self.userbenchmark_api.session.query(Metric).filter(Metric.part_id == userbenchmark_id).first()

            if metric != None:
                entities.append(GPU(metric.gaming_percentage, 
                                        metric.desktop_percentage, 
                                        metric.workstation_percentage,
                                        rank,
                                        benchmark, 
                                        samples,
                                        userbenchmark_id,
                                        pcpartpicker_id,
                                        fps_data))
        return entities 

    ###
    def get_parts_with_price(self, part_name: str):
        subquery = self.pcpartpicker_api.session.query(1).filter(PriceEntity.part_id == PcPartPickerPartEntity.id).exists()
        query = self.pcpartpicker_api.session.query(PcPartPickerPartEntity).filter(subquery)
        parts = query.filter_by(part_type = part_name).all()

        return parts
    ###
    
    ###
    def get_case_entities(self):
        case_entitities: List[(PcPartPickerPartEntity,
                                    CaseData, 
                                    List[CaseDriveBay], 
                                    List[CaseExpansionSlot], 
                                    List[CaseMotherboardFormFactor])] = []
        for case_part in self.get_parts_with_price("case"):
            case_data = self.pcpartpicker_api.session.query(CaseData).filter(CaseData.part_id == case_part.id).first()
            case_drive_bay = self.pcpartpicker_api.session.query(CaseDriveBay).filter(CaseDriveBay.part_id == case_part.id).all()
            case_expansion_slot = self.pcpartpicker_api.session.query(CaseExpansionSlot).filter(CaseExpansionSlot.part_id == case_part.id).all()
            case_motherboard_form_factor = self.pcpartpicker_api.session.query(CaseMotherboardFormFactor).filter(CaseMotherboardFormFactor.part_id == case_part.id).all()
            case_entitities.append((case_part, case_data, case_drive_bay, case_expansion_slot, case_motherboard_form_factor))
        return case_entitities
        
    ###
    def get_case_fan_entities(self):
        case_fan_entitities: List[(PcPartPickerPartEntity, 
                                        CaseFanData, 
                                        List[CaseFanConnector])] = []
        for case_fan_part in self.get_parts_with_price("case-fan"):
            case_fan_data = self.pcpartpicker_api.session.query(CaseFanData).filter(CaseFanData.part_id == case_fan_part.id).first()
            case_fan_connector = self.pcpartpicker_api.session.query(CaseFanConnector).filter(CaseFanConnector.part_id == case_fan_part.id).all()
            case_fan_entitities.append((case_fan_part, case_fan_data, case_fan_connector))
        return case_fan_entitities
        
    ###
    def get_power_supply_entities(self):
        power_supply_entitities: List[(PcPartPickerPartEntity, 
                                            PowerSupplyData, 
                                            List[PowerSupplyConnectors], 
                                            List[PowerSupplyOutput])] = []
        for power_supply_part in self.get_parts_with_price("power-supply"):
            power_supply_data = self.pcpartpicker_api.session.query(PowerSupplyData).filter(PowerSupplyData.part_id == power_supply_part.id).first()
            power_supply_connectors = self.pcpartpicker_api.session.query(PowerSupplyConnectors).filter(PowerSupplyConnectors.part_id == power_supply_part.id).all()
            power_supply_output = self.pcpartpicker_api.session.query(PowerSupplyOutput).filter(PowerSupplyOutput.part_id == power_supply_part.id).all()
            power_supply_entitities.append((power_supply_part, power_supply_data, power_supply_connectors, power_supply_output))
        return power_supply_entitities
        
    ###
    def get_motherboard_entities(self):
        motherboard_entitities: List[(PcPartPickerPartEntity, 
                                           MotherboardMainData, 
                                           List[MotherboardMemorySpeed], 
                                           List[MotherboardSocket], 
                                           List[MotherboardM2Slots], 
                                           List[MotherboardConnectData])] = []
        for motherboard_part in self.get_parts_with_price("motherboard"):
            motherboard_data = self.pcpartpicker_api.session.query(MotherboardMainData).filter(MotherboardMainData.part_id == motherboard_part.id).first()
            motherboard_memory_speed = self.pcpartpicker_api.session.query(MotherboardMemorySpeed).filter(MotherboardMemorySpeed.part_id == motherboard_part.id).all()
            motherboard_socket = self.pcpartpicker_api.session.query(MotherboardSocket).filter(MotherboardSocket.part_id == motherboard_part.id).all()
            motherboard_m2_slots = self.pcpartpicker_api.session.query(MotherboardM2Slots).filter(MotherboardM2Slots.part_id == motherboard_part.id).all()
            motherboard_connect_data = self.pcpartpicker_api.session.query(MotherboardConnectData).filter(MotherboardConnectData.part_id == motherboard_part.id).all()
            motherboard_entitities.append((motherboard_part, 
                                                motherboard_data, 
                                                motherboard_memory_speed, 
                                                motherboard_socket, 
                                                motherboard_m2_slots, 
                                                motherboard_connect_data))
        return motherboard_entitities
        
    ###
    def get_gpu_entities(self):
        gpu_parts: List[(PcPartPickerPartEntity, UserBenchmarkPartEntity)] = ConfigureMapper.get_concrent_compatible_parts("GPU")
        gpu_entitities: List[(PcPartPickerPartEntity, 
                                   UserBenchmarkPartEntity,
                                   GPUMainData, 
                                   List[GPUConnectData], 
                                   List[GPUExternalPowerData])] = []
        for gpu_part, userbenchmark_part in gpu_parts:
            gpu_main_data = self.pcpartpicker_api.session.query(CPUMainDataEntity).filter(CPUMainDataEntity.part_id == gpu_part.id).first()
            gpu_connect_data = self.pcpartpicker_api.session.query(GPUConnectData).filter(GPUConnectData.part_id == gpu_part.id).all()
            gpu_external_power = self.pcpartpicker_api.session.query(GPUExternalPowerData).filter(GPUExternalPowerData.part_id == gpu_part.id).all()
            gpu_entitities.append((gpu_part, 
                                        userbenchmark_part,
                                        gpu_main_data,
                                        gpu_connect_data,
                                        gpu_external_power))
        return gpu_entitities
        
    ###
    def get_cpu_entities(self):
        cpu_parts: List[(PcPartPickerPartEntity, UserBenchmarkPartEntity)] = ConfigureMapper.get_concrent_compatible_parts("CPU")
        cpu_entitities: List[(PcPartPickerPartEntity, 
                                   UserBenchmarkPartEntity,
                                   CPUMainDataEntity, 
                                   CPUCoreEntity)] = []
        for cpu_part, userbenchmark_part in cpu_parts:
            cpu_main_data = self.pcpartpicker_api.session.query(CPUMainDataEntity).filter(CPUMainDataEntity.part_id == cpu_part.id).first()
            cpu_core = self.pcpartpicker_api.session.query(CPUCoreEntity).filter(CPUCoreEntity.part_id == cpu_part.id).first()
            cpu_entitities.append((cpu_part, 
                                   userbenchmark_part,
                                   cpu_main_data,
                                   cpu_core))
        return cpu_entitities
        
    ###
    def get_ram_entities(self):
        ram_parts: List[(PcPartPickerPartEntity, UserBenchmarkPartEntity)] = ConfigureMapper.get_concrent_compatible_parts("RAM")
        ram_entitities: List[(PcPartPickerPartEntity, 
                                   UserBenchmarkPartEntity,
                                   MemoryMainData, 
                                   MemoryCharacteristics)] = []
        for ram_part, userbenchmark_part in ram_parts:
            memory_main_data = self.pcpartpicker_api.session.query(MemoryMainData).filter(MemoryMainData.part_id == ram_part.id).first()
            memory_characteristics = self.pcpartpicker_api.session.query(MemoryCharacteristics).filter(MemoryCharacteristics.part_id == ram_part.id).first()
            ram_entitities.append((ram_part, 
                                        userbenchmark_part,
                                        memory_main_data,
                                        memory_characteristics))
        return ram_entitities
        
    ###
    def get_ssd_entities(self):
        ssd_parts: List[(PcPartPickerPartEntity, UserBenchmarkPartEntity)] = ConfigureMapper.get_concrent_compatible_parts("SSD")
        ssd_entitities: List[(PcPartPickerPartEntity, 
                                   UserBenchmarkPartEntity,
                                   SSD)] = []
        for ssd_part, userbenchmark_part in ssd_parts:
            ssd = self.pcpartpicker_api.session.query(SSD).filter(SSD.part_id == ssd_part.id).first()
            ssd_entitities.append((ssd_part,
                                        userbenchmark_part, 
                                        ssd))
        return ssd_entitities
        
    ###
    def get_hdd_entities(self):
        hdd_parts: List[(PcPartPickerPartEntity, UserBenchmarkPartEntity)] = ConfigureMapper.get_concrent_compatible_parts("HDD")
        hdd_entitities: List[(PcPartPickerPartEntity, 
                                   UserBenchmarkPartEntity,
                                   HDD)] = []
        for hdd_part, userbenchmark_part in hdd_parts:
            hdd = self.pcpartpicker_api.session.query(HDD).filter(HDD.part_id == hdd_part.id).first()
            hdd_entitities.append((hdd_part, 
                                        userbenchmark_part,
                                        hdd))
        return hdd_entitities
        
    ###
    def get_cpu_cooler_entities(self):
        cpu_cooler_entitities: List[(PcPartPickerPartEntity, 
                                          CPUCoolerData, 
                                          List[CPUCoolerSocket])] = []
        for cpu_cooler_part in self.get_parts_with_price("cpu-cooler"):
            cpu_cooler_data = self.pcpartpicker_api.session.query(CPUCoolerData).filter(CPUCoolerData.part_id == cpu_cooler_part.id).first()
            cpu_cooler_socket = self.pcpartpicker_api.session.query(CPUCoolerSocket).filter(CPUCoolerSocket.part_id == cpu_cooler_part.id).all()
            cpu_cooler_entitities.append((cpu_cooler_part, 
                                               cpu_cooler_data, 
                                               cpu_cooler_socket))
        return cpu_cooler_entitities

    def get_concrent_compatible_parts(part_type: str):
        engine = create_engine(f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}?charset=utf8mb4")
        Session = sessionmaker(bind=engine)
        session = Session()

        sql_query = text(f"call configure_data.get_compatible_concrent_type(:type);")
        result = session.execute(sql_query, {'type': part_type })

        entities = []
        for result_tuple in result:
            pcpartpicker_entity = PcPartPickerPartEntity(
                id=result_tuple[0],
                manufacturer=result_tuple[1],
                name=result_tuple[2],
                link=result_tuple[3],
                part_type=result_tuple[4],
                key=result_tuple[5]
            )

            userbenchmark_entity = UserBenchmarkPartEntity(
                id=result_tuple[6],
                type=result_tuple[7],
                part_number=result_tuple[8],
                brand=result_tuple[9],
                model=result_tuple[10],
                rank=result_tuple[11],
                benchmark=result_tuple[12],
                samples=result_tuple[13],
                url=result_tuple[14]
            )

            entities.append((pcpartpicker_entity, userbenchmark_entity))

        session.close()
        return entities
    
    def get_all_compatible_parts():
        engine = create_engine(f"mysql://{USER_NAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}?charset=utf8mb4")
        Session = sessionmaker(bind=engine)
        session = Session()

        sql_query = text(f"call configure_data.get_compatible_parts;")
        result = session.execute(sql_query)

        entities = []
        for result_tuple in result:
            pcpartpicker_entity = PcPartPickerPartEntity(
                id=result_tuple[0],
                manufacturer=result_tuple[1],
                name=result_tuple[2],
                link=result_tuple[3],
                part_type=result_tuple[4],
                key=result_tuple[5]
            )

            userbenchmark_entity = UserBenchmarkPartEntity(
                id=result_tuple[6],
                type=result_tuple[7],
                part_number=result_tuple[8],
                brand=result_tuple[9],
                model=result_tuple[10],
                rank=result_tuple[11],
                benchmark=result_tuple[12],
                samples=result_tuple[13],
                url=result_tuple[14]
            )

            entities.append((pcpartpicker_entity, userbenchmark_entity))

        session.close()
        return entities

class ConfigureCompatibile:
    # проблемы cpu
    # нету tdp у cooler
    # нету типа памяти у cpu
    # может добавить проверку ecc?
    # может добавить проверку на maximum supported memory?
    def get_compatible_cpu_cooler(self):
        api = PcPartPickerDatabaseAPI()

        cooler_parts = api.session.query(PcPartPickerPartEntity).filter_by(part_type = "cpu-cooler")
        cooler_tuples = []
        for cooler_part in cooler_parts:
            cooler_data = api.session.query(CPUCoolerData).filter(CPUCoolerData.part_id == cooler_part.id).first()
            cooler_sockets = api.session.query(CPUCoolerSocket).filter(CPUCoolerSocket.part_id == cooler_part.id).all()
            cooler_tuples.append((cooler_data, cooler_sockets))

        compatible_parts = []
        for pcpartpicker_cpu_part, userbenchmark_cpu_part in self.cpu_parts:
            core_entity = api.session.query(CPUCoreEntity).filter(CPUCoreEntity.part_id == pcpartpicker_cpu_part.id).first()
            main_data_entity = api.session.query(CPUMainDataEntity).filter(CPUMainDataEntity.part_id == pcpartpicker_cpu_part.id).first()
            
            for cooler_data, cooler_sockets in cooler_tuples:
                socket_compatible = False
                
                # проверка по сокету
                for socket in cooler_sockets:
                    if core_entity.socket == socket.socket:
                        socket_compatible = True
                        break
                
                if socket_compatible == True:
                    compatible_parts.append({ "cpu_part_id": pcpartpicker_cpu_part.id, 
                                              "cooler_part_id": cooler_data.part_id,
                                              "socket": core_entity.socket,
                                              "includes_cooler": main_data_entity.includes_cooler })

        return compatible_parts

    def get_compatible_cpu_memory(self):
        api = PcPartPickerDatabaseAPI()

        memory_tuples = []
        for pcpartpicker_memory_part, userbenchmark_memory_part in self.ram_parts:
            memory_main_data = api.session.query(MemoryMainData).filter(MemoryMainData.part_id == pcpartpicker_memory_part.id).first()
            memory_characteristics = api.session.query(MemoryCharacteristics).filter(MemoryCharacteristics.part_id == pcpartpicker_memory_part.id).first()
            memory_tuples.append((memory_main_data, memory_characteristics))

        cpu_parts = api.session.query(PcPartPickerPartEntity).filter_by(part_type = "cpu")
        compatible_parts = []
        for pcpartpicker_cpu_part, userbenchmark_cpu_part in self.cpu_parts:
            core_entity = api.session.query(CPUCoreEntity).filter(CPUCoreEntity.part_id == pcpartpicker_cpu_part.id).first()
            main_data_entity = api.session.query(CPUMainDataEntity).filter(CPUMainDataEntity.part_id == pcpartpicker_cpu_part.id).first()

        return compatible_parts
    
    # просчитывает так, что если общая память больше максимальной то вариант сразу откидывается
    # если в пачке больше памяти чем слотов на материнки то сразу откидывается
    # можно ли как то это решить, и просчитывать все возможные варианты
    # добавить ли проверку ecc?
    def get_compatible_memory_motherboard(self):
        api = PcPartPickerDatabaseAPI()

        memory_tuples = []
        for pcpartpicker_memory_part, userbenchmark_memory_part in self.ram_parts:
            memory_main_data = api.session.query(MemoryMainData).filter(MemoryMainData.part_id == pcpartpicker_memory_part.id).first()
            memory_characteristics = api.session.query(MemoryCharacteristics).filter(MemoryCharacteristics.part_id == pcpartpicker_memory_part.id).first()
            memory_tuples.append((memory_main_data, memory_characteristics))

        motherboard_parts = api.session.query(PcPartPickerPartEntity).filter_by(part_type = "motherboard").all()
        compatible_parts = []
        for motherboard_part in motherboard_parts:
            motherboard_main_data = api.session.query(MotherboardMainData).filter(MotherboardMainData.part_id == motherboard_part.id).first()
            #motherboard_connect_data = api.session.query(MotherboardConnectData).filter(MotherboardConnectData.part_id == motherboard_part.id).first()

            motherboard_memory_speed_entities = api.session.query(MotherboardMemorySpeed).filter(MotherboardMemorySpeed.part_id == motherboard_part.id).all()
            #motherboard_socket_entities = api.session.query(MotherboardSocket).filter(MotherboardSocket.part_id == motherboard_part.id).all()

            for memory_main_data, memory_characteristics in memory_tuples:
                compatible = False

                # проверка по типу памяти
                if motherboard_main_data.memory_type == memory_characteristics.memory_type:
                    # рассчет общей памяти набора памяти
                    if memory_characteristics.modules_memory_measure == "GB":
                        total_memory = memory_characteristics.modules_count * memory_characteristics.modules_memory
                    else:
                        total_memory = memory_characteristics.modules_count * memory_characteristics.modules_memory / 1000

                    # проверка по максимальному кол-ву памяти и по максимальному кол-ву слотов памяти
                    if total_memory > motherboard_main_data.memory_max or memory_characteristics.modules_count > motherboard_main_data.memory_slots:
                        compatible = False
                    else:
                        compatible = True

                    if compatible == True:
                        # рассчет мин и макс скорости памяти для двух комплектующих
                        max_available_memory_speed = 0
                        min_available_memory_speed = motherboard_memory_speed_entities[0].memory_speed
                        for memory_speed_entity in motherboard_memory_speed_entities:
                            if (memory_speed_entity.memory_type == memory_characteristics.memory_type and 
                                memory_speed_entity.memory_speed > max_available_memory_speed):
                                max_available_memory_speed = memory_speed_entity.memory_speed

                            if (memory_speed_entity.memory_type == memory_characteristics.memory_type and 
                                memory_speed_entity.memory_speed < min_available_memory_speed):
                                min_available_memory_speed = memory_speed_entity.memory_speed

                        compatible_parts.append({
                            "memory_part_id": memory_main_data.part_id,
                            "motherboard_part_id": motherboard_main_data.part_id,
                            "max_available_memory_speed": max_available_memory_speed,
                            "min_available_memory_speed": min_available_memory_speed
                        })

        return compatible_parts
    
    def get_compatible_case_motherboard(self):
        api = PcPartPickerDatabaseAPI()

        cases = []
        case_parts = api.session.query(PcPartPickerPartEntity).filter_by(part_type = "case").all()
        for case_part in case_parts:
            case_motherboard_form_factor = api.session.query(CaseMotherboardFormFactor).filter(CaseMotherboardFormFactor.part_id == case_part.id).all()
            case_data = api.session.query(CaseData).filter(CaseData.part_id == case_part.id).first()
            cases.append((case_data, case_motherboard_form_factor))

        compatible_parts = []
        motherboard_parts = api.session.query(PcPartPickerPartEntity).filter_by(part_type = "motherboard").all()
        for motherboard_part in motherboard_parts:
            motherboard_main_data = api.session.query(MotherboardMainData).filter(MotherboardMainData.part_id == motherboard_part.id).first()
            
            for case_data, case_motherboard_form_factor in cases:
                motherboard_compatible = False
                
                # проверка по форм фактору
                common_form_factor = None
                for form_factor in case_motherboard_form_factor:
                    if motherboard_main_data.form_factor == form_factor.value:
                        motherboard_compatible = True
                        common_form_factor = motherboard_main_data.form_factor
                        break
                
                if motherboard_compatible == True:
                    compatible_parts.append({ "motherboard_part_id": motherboard_part.id, 
                                              "case_part_id": case_data.part_id,
                                              "form_factor": common_form_factor })
                    
        return compatible_parts
    
    def get_compatible_motherboard(self):
        self.__init_motherboard()
        self.__init_case()
        self.__init_cpu()
        self.__init_cpu_cooler()
        self.__init_ssd()
        self.__init_power_supply()
        self.__init_ram()
        self.__init_gpu()
        self.__init_hdd()

        print(len(self.case_entitities))
        print(len(self.cpu_cooler_entitities))
        print(len(self.motherboard_entitities))
        print(len(self.power_supply_entitities))
        print()
        print(len(self.cpu_entitities))
        print(len(self.gpu_entitities))
        print(len(self.ram_entitities))
        print(len(self.hdd_entitities))
        print(len(self.ssd_entitities))

        for (motherboard_part, 
             motherboard_data, 
             motherboard_memory_speed, 
             motherboard_socket, 
             motherboard_m2_slots, 
             motherboard_connect_data) in self.motherboard_entitities:
            pass
    
    # делаем compatible cpu, gpu, ram, hdd, ssd
    # motherboard_main_data.memory_type
    # motherboard_connect_data
    # точно есть набор этих комплектующих которые нельзя запустить ни на одной материнке,
    # ни с одним powersupply
    def get_compatible_main_config_data(self):
        self.__init_cpu()
        self.__init_gpu()
        self.__init_ram()
        #self.__init_hdd()
        #self.__init_ssd()

        self.cpu_entitities
        self.gpu_entitities
        self.ram_entitities
        #self.hdd_entitities
        #self.ssd_entitities

        # по сути то тут зависимостей и нету
        # cpu -> memory (через материнку)
        # gpu -> memory, cpu (через материнку)
        pass
    
    # совмещаем две совместиомсти отдельно
    
    # делаем compatible case, cpu_cooler, power_supply, case_fan
    def get_compatible_all_config_data(self):
        pass