import logging

from src.pcpartpicker.PcPartPickerLinks import PcPartPickerLinks

LOG_PATH = "data\\pcpartpicker\\logs\\pcpartpicker_links.log"

logging.basicConfig(level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
encoding='utf-8')
logger = logging.getLogger("pcpartpicker_links")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

parser = PcPartPickerLinks(logger)
with parser:
    parser.get_all_links()