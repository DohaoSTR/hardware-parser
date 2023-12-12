from src.userbenchmark.mapper.DatabaseAPI import DatabaseAPI as UserBenchmarkDatabaseAPI
from src.pcpartpicker.DatabaseAPI import DatabaseAPI as PcPartPickerDatabaseAPI

import time

HOST = "localhost"
USER_NAME = "root"
PASSWORD = "root"
DATABASE_NAME = "pcpartpicker_userbenchmark_data"

# подумать как сделать конфигуратор

# делать весь конфиг в бд немного не выгодно, потому что нельзя обработать значения

# точно надо обработать ключи в бд

# как я считаю нужно просчитать совместимость отдельных комплектующих
# загрузить это либо в файл либо в бд
# и уже от этих данных собирать модель уравнений

class RelationMapper:
    def compare_pcpartpicker_userbenchmark_parts():
        pass