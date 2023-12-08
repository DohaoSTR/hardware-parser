from dataclasses import dataclass
import re

from ..BaseEntity import BaseEntity

from ..db_entities.Memory.MemoryMainData import MemoryMainData
from ..db_entities.Memory.MemoryCharacteristics import MemoryCharacteristics

@dataclass
class PcPartPickerMemoryEntity(BaseEntity):
    speed: str = None
    memory_speed: int = None
    memory_type: str = None

    form_factor: str = None
    pin_count: int = None
    memory_form_factor: str = None

    modules: str = None
    modules_count: int = None
    modules_memory: int = None
    modules_memory_measure: str = None

    price: str = None
    currency: str = None
    price_gb: float = None

    color: str = None

    first_word_latency: float = None

    cas_latency: float = None

    voltage: float = None

    timing: str = None
    cas: int = None
    trcd: int = None
    trp: int = None
    tras: int = None

    ecc_registered: str = None
    register_memory: str = None
    ecc: str = None

    heat_spreader: str = None
    model: str = None

    memory_main_data: MemoryMainData = None
    memory_characteristics: MemoryCharacteristics = None

    def __post_init__(self):
        self.memory_type, self.memory_speed = self.handle_speed(self.speed)
        self.pin_count, self.memory_form_factor = self.handle_form_factor(self.form_factor)
        self.modules_count, self.modules_memory, self.modules_memory_measure = self.handle_modules_string(self.modules)

        self.currency, self.price_gb = self.handle_price_gb(self.price)

        self.first_word_latency = self.handle_parameter(self.first_word_latency, float, "ns")
        self.voltage = self.handle_parameter(self.voltage, float, "V")
        self.cas, self.trcd, self.trp, self.tras = self.transform_string(self.timing)
        self.ecc, self.register_memory = self.handle_memory_type(self.ecc_registered)

        self.cast_int_fields()
        self.cast_float_fields()

        self.memory_main_data = self.populate_entity("MemoryMainData", "part_id")
        self.memory_characteristics = self.populate_entity("MemoryCharacteristics", "memory_id")

    def handle_speed(self, memory_string):
        if memory_string != None:
            parts = memory_string.split("-")

            if len(parts) == 2:
                return parts[0], parts[1]
            else:
                return None, None
        else:
            return None, None
        
    def handle_form_factor(self, memory_string):
        if memory_string != None:
            match = re.match(r"(\d+)-pin\s+(\w+)", memory_string)

            if match:
                number, text = match.groups()
                number = int(number)
                return number, text
            else:
                return None, None
        else:           
            return None, None
        
    def handle_modules_string(self, modules_string):
        if modules_string != None:
            match = re.match(r"(\d+)\s*x\s*(\d+)(..)", modules_string)
            if match:
                amount = int(match.group(1))
                size = int(match.group(2))
                measure = match.group(3)
                return amount, size, measure
            else:
                raise ValueError("Couldn't parse string")
        else:           
            return None, None, None
    
    def transform_string(self, input_string):
        if input_string != None:
            parts = input_string.split("-")
            int_values = [int(part) for part in parts]

            return tuple(int_values)
        else:
            return None, None, None, None
    
    def handle_memory_type(self, memory_string):
        if memory_string != None:
            parts = memory_string.split(" / ")
            ecc = "No" if "Non-ECC" in parts[0] else "Yes"
            register_memory = "Yes" if "Registered" in parts[1] else "No"

            return ecc, register_memory
        else:
            return None, None