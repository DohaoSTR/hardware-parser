from src.userbenchmark.Resolution import Resolution
from src.userbenchmark.FPSCombination import FPSCombination
from src.userbenchmark.GameSettings import GameSettings
from src.userbenchmark.AsyncFPSData import AsyncFPSData

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

parser = AsyncFPSData(logger)

selected_combinations = [FPSCombination.CPU, FPSCombination.GPU, FPSCombination.GPU_CPU]
selected_game_settings = [GameSettings.NONE, GameSettings.LOW,  GameSettings.MED, GameSettings.HIGH, GameSettings.MAX]
selected_resolutions = [Resolution.NONE, Resolution.HD_720p, Resolution.FULL_HD_1080p, Resolution.QHD_1440p]
parser.auto_parsing(selected_combinations, selected_game_settings, selected_resolutions)