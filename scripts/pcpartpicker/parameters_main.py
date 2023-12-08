import logging

from src.pcpartpicker.PcPartPickerParameters import PcPartPickerParameters

LOG_PATH = "data\\pcpartpicker\\logs\\pcpartpicker_parser.log"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8')
    logger = logging.getLogger("pcpartpicker_parser")
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    parser = PcPartPickerParameters(logger)
    with parser:
        parser.get_all_pages_data()