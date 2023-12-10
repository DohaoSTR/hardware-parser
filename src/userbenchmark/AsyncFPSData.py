from .UserBenchmarkRequest import UserBecnhmarkRequest

from .FPSCombination import FPSCombination
from .GameSettings import GameSettings
from .Part import Part
from .Resolution import Resolution

from .KeysHandling import KeysHandling
from .GameKeys import GameKeys

from ..TorManager import TorManager

import logging
from logging import Logger

import json
import concurrent.futures
import threading

from bs4 import BeautifulSoup
import os

GAMES_TO_PARSE_COUNT = 35
THREADS_COUNT = 8

# класс для получения fps данных
# async класс
class AsyncFPSData:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        self.lock = threading.Lock()

        web_driver = UserBecnhmarkRequest(logger, is_multi_threading=True)
        web_driver.set_async(self)
        self.web_driver = web_driver

        self.tor_manager = TorManager(logger)

        self.link = None
        self.fps_data = None

    # реакция при окончании работы или возникновение ошибки
    def __exit__(self, exc_type, exc_value, traceback):
        if self.link != None:
            self.logger.info(f"Работа парсера завершена, Link: {self.link}")
        
        if self.fps_data != None:
            self.logger.info(f"Последний объект - fps_data: {self.fps_data}")

        self.logger.info("Параметры метода __exit__:")
        self.logger.info(f"Тип возникшего исключения: {exc_type}")
        self.logger.info(f"Значение исключения: {exc_value}")
        self.logger.info(f"Объект traceback: {traceback}")

        with self.lock:
            self.tor_manager.close_tor()

        self.logger.info("Вызван метод __exit__, ресурсы очищены.")

    def __enter__(self):
        return self

    # метод для получения fps и кол-ва тестов с страницы
    def __get_fps_samples_from_page(self, link):
        self.link = link

        try:
            html_content = self.web_driver.get_html_content(link)
            if (html_content == None):
                self.logger.info(f"{link} - HTML контент равен None.")
                return None, None
            
            soup = BeautifulSoup(html_content, 'html.parser')

            fps_element = soup.find('h3', class_='text-center blacktext')
            fps_text = fps_element.get_text()

            parts = fps_text.split()

            if "only" in fps_text:
                fps_value = parts[2]
                samples_value = parts[-2]
            else:
                fps_value = parts[2]
                samples_value = parts[3]

            return fps_value, samples_value
        except AttributeError:
            self.logger.info(f"Произошла ошибка: AttributeError. __get_fps_samples_from_page")
        except Exception as e:
            self.logger.error(f"Произошла ошибка (Exception catch): {str(e)}. __get_fps_samples_from_page")

        return None, None
    
    # метод для формирования ссылки с fps данными
    def __form_fps_link(self, game_key, gpu_key, cpu_key, 
                        game_settings: GameSettings, 
                        resolution: Resolution):
        link = "https://www.userbenchmark.com/pages/product.xhtml?product_id=" + str(game_key) + "&fps_key=" + str(gpu_key) + "." + str(cpu_key) + "." + game_settings.value + "." + resolution.value + ".0"

        return link

    # метод для получения названия файла
    def __form_fps_file_name(game_key, game_settings, resolution, combination: FPSCombination):
        file_name = f"{combination.value}_{game_key}_{game_settings.value}_{resolution.value}"
        
        return file_name
    
    # получение данных из json файла
    def get_fps_data_from_json(game_key, 
                               game_settings: GameSettings, 
                               resolution: Resolution, 
                               combination: FPSCombination):
        fps_file_name = AsyncFPSData.__form_fps_file_name(game_key, game_settings, resolution, combination)
        end_folder = combination.value + "_" + game_settings.value + "_" + resolution.value + "\\"

        current_directory = os.getcwd()
        current_file_path = current_directory + "\\data\\userbenchmark\\fps_in_games\\" + end_folder

        try:
            with open(current_file_path + fps_file_name + '.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            return None
        
        return data

    # сохранение данных в файл
    def save_fps_data_to_json(game_key, 
                              game_settings: GameSettings, 
                              resolution: Resolution, 
                              combination: FPSCombination, 
                              data):
        fps_data = AsyncFPSData.get_fps_data_from_json(game_key, game_settings, resolution, combination)

        if fps_data == None:
            existing_data = {}
        else:
            existing_data = fps_data

        existing_data.update(data)

        fps_file_name = AsyncFPSData.__form_fps_file_name(game_key, game_settings, resolution, combination)
        end_folder = combination.value + "_" + game_settings.value + "_" + resolution.value + "\\"

        current_directory = os.getcwd()
        current_file_path = current_directory + "\\data\\userbenchmark\\fps_in_games\\" + end_folder

        if not os.path.exists(current_file_path):
            os.makedirs(current_file_path)

        with open(current_file_path + fps_file_name + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, indent=4, ensure_ascii=False)

    # получение всех fps данных для игры
    def __get_fps_data_for_game(self, game_key, gpu_fps_keys, cpu_fps_keys, 
                                game_settings: GameSettings, 
                                resolution: Resolution, 
                                fps_combination: FPSCombination, last_index = 0):
        fps_data = {}
        
        index = last_index
        for cpu_key in cpu_fps_keys:
            for gpu_key in gpu_fps_keys:
                link = self.__form_fps_link(game_key, gpu_key, cpu_key, game_settings, resolution)  

                result = self.__get_fps_samples_from_page(link)
                if result is not None:
                    fps_value, samples_value = result
                else:
                    self.logger.info(f"result равен None, __get_fps_data_for_game: {link}")

                if fps_value is not None or samples_value is not None:
                    fps_value = fps_value.replace(",", ".")
                    samples_value = samples_value.replace(",", "")

                    self.fps_data = {
                                    "game_key": game_key, "gpu_key": gpu_key, 
                                    "cpu_key": cpu_key,  "fps_value": float(fps_value), 
                                    "samples_value": int(samples_value), 
                                    "game_settings": game_settings.value, 
                                    "resolution": resolution.value,                                
                                    }
                    data = { "gpu_key": int(gpu_key), "cpu_key": int(cpu_key), "fps_value": float(fps_value), "samples_value": int(samples_value) }
                    fps_data[str(index)] = data
                        
                    self.logger.info(f"{index}. Данные - {fps_data[str(index)]}")
                else:
                    self.fps_data = {
                                    "game_key": game_key, "gpu_key": gpu_key, 
                                    "cpu_key": cpu_key,  "fps_value": None, 
                                    "samples_value": None, 
                                    "game_settings": game_settings.value, 
                                    "resolution": resolution.value,                                
                                    }
                    data = { "gpu_key": int(gpu_key), "cpu_key": int(cpu_key), "fps_value": None, "samples_value": None }
                    fps_data[str(index)] = data

                    self.logger.info(f"{index}. На странице нет данных.")

                self.logger.info(f"Ссылка: {link}")
                
                index = index + 1
                if index % 100 == 0:
                    AsyncFPSData.save_fps_data_to_json(game_key, game_settings, resolution, fps_combination, fps_data)

        AsyncFPSData.save_fps_data_to_json(game_key, game_settings, resolution, fps_combination, fps_data)
        return fps_data
    
    # запуск паралельного парсера
    def parallel_parse_data(self, game_keys, gpu_fps_keys, cpu_fps_keys, game_settings, resolution, fps_combination: FPSCombination):
        futures = []
        event = threading.Event()

        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS_COUNT) as executor:
            for game_key in game_keys:
                missing_keys = AsyncFPSData.get_missing_keys(game_key, fps_combination, game_settings, resolution)
                last_index = 0
                
                if missing_keys == None:
                    future = executor.submit(self.__get_fps_data_for_game, game_key, gpu_fps_keys, cpu_fps_keys, game_settings, resolution, fps_combination, last_index)
                    futures.append(future)
                elif missing_keys == [] or len(missing_keys) == 0:
                    pass
                else:
                    if fps_combination == FPSCombination.GPU:
                        gpu_fps_keys = missing_keys  
                        cpu_fps_keys = [0]
                    elif fps_combination == FPSCombination.CPU:
                        cpu_fps_keys = missing_keys
                        gpu_fps_keys = [0]
                    elif fps_combination == FPSCombination.GPU_CPU:
                        gpu_fps_keys = []
                        cpu_fps_keys = []

                        for key_item in missing_keys:
                            if len(key_item) == 2:
                                gpu_key, cpu_key = key_item
                                gpu_fps_keys.append(gpu_key)
                                cpu_fps_keys.append(cpu_key)

                    last_index = AsyncFPSData.get_last_index_from_json_file(game_key, fps_combination, game_settings, resolution) + 1

                    future = executor.submit(self.__get_fps_data_for_game, game_key, gpu_fps_keys, cpu_fps_keys, game_settings, resolution, fps_combination, last_index)
                    futures.append(future)

            event.set()

        event.wait()

        for future in futures:
            future.result()

    # запуск парсера на конкретных настройках
    def parse_fps_data(self, 
                       combination: FPSCombination, 
                       game_settings: GameSettings, 
                       resolution: Resolution):
        game_keys = GameKeys.get_game_keys_from_json()
        game_keys_list = list(game_keys.keys())
        game_keys = game_keys_list[:GAMES_TO_PARSE_COUNT]

        if combination == FPSCombination.GPU:
            fps_keys = KeysHandling.get_handled_part_keys_from_json(Part.GPU)

            gpu_fps_keys_list = [entry["key"] for entry in fps_keys.values()]
            cpu_fps_keys_list = [0]
        elif combination == FPSCombination.CPU:
            fps_keys = KeysHandling.get_handled_part_keys_from_json(Part.CPU)

            gpu_fps_keys_list = [0]
            cpu_fps_keys_list = [entry["key"] for entry in fps_keys.values()]
        elif combination == FPSCombination.GPU_CPU:
            gpu_fps_keys = KeysHandling.get_handled_part_keys_from_json(Part.GPU)
            cpu_fps_keys = KeysHandling.get_handled_part_keys_from_json(Part.CPU)

            gpu_fps_keys_list = [entry["key"] for entry in gpu_fps_keys.values()]
            cpu_fps_keys_list = [entry["key"] for entry in cpu_fps_keys.values()]

        self.parallel_parse_data(game_keys, gpu_fps_keys_list, cpu_fps_keys_list, game_settings, resolution, combination)

    # метод возвращающий все ключи которых не хватает в файле c фпс данными
    def get_missing_keys(game_key: int, 
                         combination: FPSCombination, 
                         game_settings: GameSettings, 
                         resolution: Resolution):
        fps_data = AsyncFPSData.get_fps_data_from_json(game_key, game_settings, resolution, combination)

        if fps_data == None or len(fps_data) == 0:
            return None

        if combination == FPSCombination.GPU_CPU:
            handled_cpu_keys_data = KeysHandling.get_handled_part_keys_from_json(Part.CPU)
            handled_gpu_keys_data = KeysHandling.get_handled_part_keys_from_json(Part.GPU)

            handled_cpu_keys = [int(entry["key"]) for entry in handled_cpu_keys_data.values()]
            handled_gpu_keys = [int(entry["key"]) for entry in handled_gpu_keys_data.values()]

            all_combinations = set((gpu_key, cpu_key) for cpu_key in handled_cpu_keys for gpu_key in handled_gpu_keys)
            missing_combinations = all_combinations - set((value["gpu_key"], value["cpu_key"]) for value in fps_data.values())
            missing_combinations_list = list(missing_combinations)

            return missing_combinations_list
        elif combination == FPSCombination.CPU or combination == FPSCombination.GPU:
            part = FPSCombination.PART_MAPPING.get(combination)
            handled_part_keys_data = KeysHandling.get_handled_part_keys_from_json(part)

            handled_keys = [int(entry["key"]) for entry in handled_part_keys_data.values()]
            
            key_name = FPSCombination.KEY_MAPPING.get(combination)
            part_keys = [entry[key_name] for entry in fps_data.values()]

            missing_keys = [key for key in handled_keys if key not in part_keys]

            return missing_keys

    # метод получения последнего индекса из файла
    def get_last_index_from_json_file(game_key: int, 
                                      combination: FPSCombination, 
                                      game_settings: GameSettings, 
                                      resolution: Resolution):
        fps_data = AsyncFPSData.get_fps_data_from_json(game_key, game_settings, resolution, combination)
        last_key = list(fps_data.keys())[-1]

        return int(last_key)

    def auto_parsing(self, fps_combination_enum, game_settings_enum, resolution_enum):
        for combination in fps_combination_enum:
            for game_settings in game_settings_enum:
                for resolution in resolution_enum:
                        self.parse_fps_data(combination, game_settings, resolution)