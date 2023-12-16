from dataclasses import dataclass

import json
import os
import time

from typing import List

import numpy as np

from src.configure.ConfigureMapper import CPU, GPU, ConfigureMapper, MainPart
from src.userbenchmark.mapper.db_entities.PartEntity import PartEntity as UserBenchmarkPartEntity

from enum import Enum

@dataclass
class MainConfigureData:
    part_metric: float
    cpu_id: int
    gpu_id: int
    ram_id: int

class MetricCalculationType(Enum):
    GAMING = "gaming_metric"
    DESKTOP = "desktop_metric"
    WORKSTATION = "workstation_metric"
    AVERAGE = "average_metric"

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
        self.cpu_entities = self.mapper.get_cpu_entities()
        self.gpu_entities = self.mapper.get_gpu_entities()
        self.hdd_entities = self.mapper.get_hdd_entities()
        self.ssd_entities = self.mapper.get_ssd_entities()
        self.ram_entities = self.mapper.get_ram_entities()
    
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
    
    def get_extremes(self):
        fps_data_entities = self.mapper.get_fps_data()

        max_samples = 0
        min_samples = fps_data_entities[0].samples
        for fps_data_entity in fps_data_entities:
            if fps_data_entity.samples > max_samples:
                max_samples = fps_data_entity.samples

            if fps_data_entity.samples < min_samples:
                min_samples = fps_data_entity.samples
        
        return (min_samples, max_samples)

    def get_relative_coef(self, 
                          samples_value,
                          max_samples: int, 
                          min_samples: int):
        relative_coef = ((samples_value - min_samples)/(max_samples - min_samples)) * 100
        return relative_coef

    # надо смотреть по комбинации cpu, gpu и в среднем
    # average_cpu_metric
    # average_gpu_metric
    # average_gpu_cpu_metric
    # average_metric
    def get_game_metrics(self,
                         cpu_entity: CPU,
                         gpu_entity: GPU,
                         max_samples: int,
                         min_samplse: int):
        for fps_data_item in cpu_entity.fps_data:
            relative_coef = self.get_relative_coef(fps_data_item.samples, 
                                                   max_samples, 
                                                   min_samplse)
            fps_data_item.fps
            fps_data_item.game_settings
            fps_data_item.resolution
            fps_data_item.game_key
        
        for fps_data_item in gpu_entity.fps_data:
            pass

        # cpu fps комбинации все
        # gpu fps комбинации все
        # cpu gpu 

    def get_main_configure(self, 
                           cpu_entity: MainPart,
                           gpu_entity: MainPart,
                           ram_entity: MainPart,
                           type: MetricCalculationType,
                           hdd_entities: List[MainPart] = None,
                           ssd_entities: List[MainPart] = None):
        max_hdd_metric = 0
        if hdd_entities != None and len(hdd_entities > 0):
            for hdd_entity in hdd_entities:
                metric = type.get_metric(hdd_entity)
                if metric > max_hdd_metric:
                    max_hdd_metric = metric

        max_ssd_metric = 0
        if ssd_entities != None and len(ssd_entities > 0):
            for ssd_entity in ssd_entities:
                metric = type.get_metric(ssd_entity)
                if metric > max_ssd_metric:
                    max_ssd_metric = metric
        
        return self.get_part_metric(type.get_metric(cpu_entity), 
                                    type.get_metric(gpu_entity), 
                                    type.get_metric(ram_entity),
                                    max_hdd_metric,
                                    max_ssd_metric)
    
    def save_all_combinations(self, data):
        current_directory = os.getcwd()
        current_file_path = current_directory + "\\data\\configure\\"

        with open(current_file_path + 'main_combinations.json', 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def get_all_combinations(self):
        current_directory = os.getcwd()
        current_file_path = current_directory + "\\data\\configure\\"
        
        with open(current_file_path + 'main_combinations.json', 'r', encoding="utf-8") as json_file:
            all_combinations = json.load(json_file)

        return all_combinations

    # оптимизация через методы оптимизации
    def parse_all_combinations_of_main_configure(self):
        min_samples, max_samples = self.get_extremes()
        cpu_parts = self.mapper.get_cpu_main_parts()
        gpu_parts = self.mapper.get_gpu_main_parts()
        ram_parts = self.mapper.get_ram_main_parts()

        all_combinations = []
        start_time = time.time()
        index = 0
        for cpu in cpu_parts:
            for gpu in gpu_parts:
                for ram in ram_parts:
                    # + метрики
                    average_metric = self.get_main_configure(cpu, gpu, ram, MetricCalculationType.AVERAGE)
                    desktop_metric = self.get_main_configure(cpu, gpu, ram, MetricCalculationType.DESKTOP)
                    gaming_metric = self.get_main_configure(cpu, gpu, ram, MetricCalculationType.GAMING)
                    workstation_metric = self.get_main_configure(cpu, gpu, ram, MetricCalculationType.WORKSTATION)

                    game_metrics = self.get_game_metrics(cpu, gpu)

                    all_combinations.append({
                        "cpu_id": cpu.pcpartpicker_id,
                        "gpu_id": gpu.pcpartpicker_id,
                        "ram_id": ram.pcpartpicker_id,
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
    
    # что делать если имеется материнская плата, она не main
    # что делать если cpu и memory несовместимы (что очень вероятно может быть)
    def pick_up_main_configure(self, 
                               type: MetricCalculationType,
                               cpu: CPU = None,
                               gpu: GPU = None,
                               ram: MainPart = None,
                               return_count: int = 5):
        all_combinations = self.get_all_combinations()

        optimal_data: List[MainConfigureData] = []
        max_part_metric = 0
        if cpu == None and gpu == None and ram == None:
            for combination_data in all_combinations:
                if combination_data[type.value] > max_part_metric:
                    max_part_metric = combination_data[type.value]
                    cpu_id = combination_data["cpu_id"]
                    gpu_id = combination_data["gpu_id"]
                    ram_id = combination_data["ram_id"]
                    optimal_data.append(MainConfigureData(max_part_metric, cpu_id, gpu_id, ram_id))

        return optimal_data[-return_count:]

    # метод подбора internal_drives для пользователя
    def pick_up_internal_drives(self, 
                                hdd_count: int, 
                                ssd_count: int):
        pass