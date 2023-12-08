from enum import Enum

class UserBenchmarkPart(Enum):
    CPU = "cpu"
    GPU = "gpu"
    RAM = "ram"
    SSD = "ssd"
    HDD = "hdd"