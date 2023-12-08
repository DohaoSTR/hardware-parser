from src.TorManager import TorManager

import logging
from logging import Logger

LOG_PATH = "data\\logs\\tor_manager_test.log"

def do_sequential_operation_with_tor(logger: Logger = None):
    manager = TorManager(logger)
    print(f"StartTor - {manager.start_tor()}")
    print()
    print(f"CloseTor - {manager.close_tor()}")
    print()
    print(f"StartTor - {manager.start_tor()}")
    print()
    print(f"RestartTor - {manager.restart_tor()}")

    print()
    print(f"TorConnection - {manager.check_tor_connection(8000)}")
    print(f"CloseTor - {manager.close_tor()}")

def do_operations_with_users_data():
    tor_user_data = TorManager.get_standard_user_data()
    print()
    print(f"UserData, port - {tor_user_data.port}")
    print(f"UserData, user_agent - {tor_user_data.user_agent}")

    tor_user_data = TorManager.get_random_user()
    if tor_user_data != None:
        print()
        print(f"RandomUserData, port - {tor_user_data.port}")
        print(f"RandomUserData, user_agent - {tor_user_data.user_agent}")

    users_data = TorManager.get_users_data()
    print()
    print(f"Lenght, users_data - {len(users_data)}")

    print()
    for user_data in users_data:
        print(f"UserData, port - {user_data.port}")
        print(f"UserData, user_agent - {user_data.user_agent}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8')
    logger = logging.getLogger("tor_manager")
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    do_sequential_operation_with_tor(logger)
    
    do_operations_with_users_data()