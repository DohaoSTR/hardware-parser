from dataclasses import dataclass
import re
from typing import List

from ..BaseEntity import BaseEntity

from ..db_entities.CPUCooler.CPUCoolerData import CPUCoolerData
from ..db_entities.CPUCooler.CPUCoolerSocket import CPUCoolerSocket

@dataclass
class PcPartPickerCPUCoolerEntity(BaseEntity):
    model: str = None
    fan_rpm: str = None
    noise_level: str = None
    height: float = None

    socket: str = None

    water_cooled: float = None
    fanless: str = None
    color: str = None
    bearing: str = None

    min_rpm: float = None
    max_rpm: float = None

    min_noise_level: float = None
    max_noise_level: float = None

    fan: str = None

    cooler_data: CPUCoolerData = None
    cooler_sockets: List[CPUCoolerSocket] = None

    def __populate_socket(self, value):
        if isinstance(value, list):
            sockets = []
            for item in value:
                sockets.append(CPUCoolerSocket(socket = item))
            return sockets
        elif isinstance(value, str):
            return [CPUCoolerSocket(socket = value)]
        else:
            return None

    def __post_init__(self):
        self.min_rpm, self.max_rpm = self.handle_value_with_hyphen(self.fan_rpm, "RPM")
        self.min_noise_level, self.max_noise_level = self.handle_value_with_hyphen(self.noise_level, "dB")

        self.height = self.handle_parameter(self.height, float, "mm")

        self.fan = self.handle_fanless(self.fanless)

        self.water_cooled = self.handle_water_cooled(self.water_cooled)

        self.cast_float_fields()
        self.cast_int_fields()

        self.cooler_data = self.populate_entity("CPUCoolerData", "part_id")
        self.cooler_sockets = self.__populate_socket(self.socket)

    def handle_water_cooled(self, value):
        if value == "No":
            return None
        else:
            pattern = r'(\d+)'
            match = re.search(pattern, value)
            if match:
                water_cooled = int(match.group(1))
                return water_cooled
            else:
                raise Exception()