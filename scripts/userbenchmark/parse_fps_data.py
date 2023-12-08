from src.userbenchmark.UserBenchmarkResolution import UserBenchmarkResolution
from src.userbenchmark.UserBenchmarkFPSCombination import UserBenchmarkFPSCombination
from src.userbenchmark.UserBenchmarkGameSettings import UserBenchmarkGameSettings
from src.userbenchmark.UserBenchmarkAsyncFPSData import UserBenchmarkAsyncFPSData

import logging

LOG_PATH = "data\\userbenchmark\\logs\\fps_data.log"

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                encoding='utf-8')
logger = logging.getLogger("fps_data")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

parser = UserBenchmarkAsyncFPSData(logger)

selected_combinations = [UserBenchmarkFPSCombination.CPU, UserBenchmarkFPSCombination.GPU, UserBenchmarkFPSCombination.GPU_CPU]
selected_game_settings = [UserBenchmarkResolution.NONE, UserBenchmarkGameSettings.LOW,  UserBenchmarkGameSettings.MED, UserBenchmarkGameSettings.HIGH, UserBenchmarkGameSettings.MAX]
selected_resolutions = [UserBenchmarkResolution.NONE, UserBenchmarkResolution.HD_720p, UserBenchmarkResolution.FULL_HD_1080p, UserBenchmarkResolution.QHD_1440p]
parser.auto_parsing(selected_combinations, selected_game_settings, selected_resolutions)