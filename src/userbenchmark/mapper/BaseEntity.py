from dataclasses import dataclass, fields

from src.userbenchmark.mapper.db_entities.PartUserData import PartUserData
from src.userbenchmark.mapper.db_entities.PartEntity import PartEntity
from src.userbenchmark.mapper.db_entities.CPUMetricsData import CPUMetricsData
from src.userbenchmark.mapper.db_entities.GPUMetricsData import GPUMetricsData
from src.userbenchmark.mapper.db_entities.HDDMetricsData import HDDMetricsData
from src.userbenchmark.mapper.db_entities.SSDMetricsData import SSDMetricsData
from src.userbenchmark.mapper.db_entities.RAMMetricsData import RAMMetricsData

@dataclass
class BaseEntity:
    key: int

    def populate_entity(entity, class_name, foreign_column_name):
        my_instance = globals()[class_name]
        db_entity = my_instance()

        for column_name in db_entity.__table__.columns.keys():
            if column_name != "id" and column_name != foreign_column_name:
                setattr(db_entity, column_name, getattr(entity, column_name))

        return db_entity