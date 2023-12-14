import time
from typing import List
from src.configure.ConfigureMapper import ConfigureMapper, MainPart
from src.userbenchmark.mapper.db_entities.PartEntity import PartEntity as UserBenchmarkPartEntity

from enum import Enum

class MetricCalculationType(Enum):
    GAMING = "gaming"
    DESKTOP = "desktop"
    WORKSTATION = "workstation"
    AVERAGE = "average"

    def get_metric(self, part: MainPart):
        if MetricCalculationType.AVERAGE == self:
            return (part.desktop_metric + part.gaming_metric + part.workstation_metric) / 3
        elif MetricCalculationType.DESKTOP == self:
            return part.desktop_metric
        elif MetricCalculationType.GAMING == self:
            return part.gaming_metric
        elif MetricCalculationType.WORKSTATION == self:
            return part.workstation_metric

WEIGHT_CPU_METRIC = 1
WEIGHT_GPU_METRIC = 1
WEIGHT_RAM_METRIC = 1
WEIGHT_SSD_METRIC = 1
WEIGHT_HDD_METRIC = 1

class ConfigureModel:
    def __init__(self) -> None:      
        self.mapper = ConfigureMapper()
        self.mapper.init_cpu()
        self.mapper.init_gpu()
        self.mapper.init_hdd()
        self.mapper.init_ssd()
        self.mapper.init_ram()
    
    def get_part_metric(self, 
                        cpu_metric: float, 
                        gpu_metric: float, 
                        ram_metric: float,
                        hdd_metric: float, 
                        ssd_metric: float):
        return (WEIGHT_CPU_METRIC*cpu_metric +
                WEIGHT_GPU_METRIC*gpu_metric +
                WEIGHT_RAM_METRIC*ram_metric + 
                WEIGHT_HDD_METRIC*hdd_metric + 
                WEIGHT_SSD_METRIC*ssd_metric)
    
    def get_main_configure(self, 
                           cpu_entity: MainPart,
                           gpu_entity: MainPart,
                           ram_entity: MainPart,
                           hdd_entities: List[MainPart], 
                           ssd_entities: List[MainPart],
                           type: MetricCalculationType):
        max_hdd_metric = 0
        for hdd_entity in hdd_entities:
            metric = type.get_metric(hdd_entity)
            if metric > max_hdd_metric:
                max_hdd_metric = metric

        max_ssd_metric = 0
        for ssd_entity in ssd_entities:
            metric = type.get_metric(ssd_entity)
            if metric > max_ssd_metric:
                max_ssd_metric = metric
        
        return self.get_part_metric(type.get_metric(cpu_entity), 
                                    type.get_metric(gpu_entity), 
                                    type.get_metric(ram_entity),
                                    max_hdd_metric,
                                    max_ssd_metric)
    
    # все равно нужно понять как сократить счет
    #
    
    # может тут заранее и расчитать фпс
    # что делать с ssd и hdd
    # и расчитать еще данных наверно
    def parse_all_combinations_of_main_configure(self):
        cpu_parts = self.mapper.get_cpu_main_parts()
        gpu_parts = self.mapper.get_gpu_main_parts()
        ram_parts = self.mapper.get_ram_main_parts()
        ssd_parts = self.mapper.get_ssd_main_parts()
        hdd_parts = self.mapper.get_hdd_main_parts()

        all_combinations = []
        start_time = time.time()
        index = 0
        for cpu in cpu_parts:
            for gpu in gpu_parts:
                for ram in ram_parts:
                    for ssd in ssd_parts:
                        for hdd in hdd_parts:
                            average_metric = self.get_main_configure(cpu, gpu, ram, [ssd], [hdd], MetricCalculationType.AVERAGE)
                            desktop_metric = self.get_main_configure(cpu, gpu, ram, [ssd], [hdd], MetricCalculationType.DESKTOP)
                            gaming_metric = self.get_main_configure(cpu, gpu, ram, [ssd], [hdd], MetricCalculationType.GAMING)
                            workstation_metric = self.get_main_configure(cpu, gpu, ram, [ssd], [hdd], MetricCalculationType.WORKSTATION)

                            all_combinations.append({
                                "cpu_id": cpu.pcpartpicker_id,
                                "gpu_id": gpu.pcpartpicker_id,
                                "ram_id": ram.pcpartpicker_id,
                                "ssd_id": ssd.pcpartpicker_id,
                                "hdd_id": hdd.pcpartpicker_id,
                                "average_metric": average_metric,
                                "desktop_metric": desktop_metric,
                                "gaming_metric": gaming_metric,
                                "workstation_metric": workstation_metric,
                                })
                            
                            index += 1
                            if index % 1000000 == 0:
                                end_time = time.time()
                                execution_time = end_time - start_time
                                print(f"{index} - записей обработано за {execution_time} секунд.")
                            
        return all_combinations