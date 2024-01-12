import logging
from logging import Logger

from src.userbenchmark.GameKeys import GameKeys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
logger = logging.getLogger("userbenchmark_game_keys_parser")
file_handler = logging.FileHandler("data\\logs\\userbenchmark_game_keys_parser.log")
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

parser = GameKeys(logger)
with parser:
    game_keys_data = parser.get_game_links_from_all_pages()
    GameKeys.save_game_keys_to_json(game_keys_data)