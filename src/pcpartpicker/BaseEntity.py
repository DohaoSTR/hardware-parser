from dataclasses import dataclass, fields

from src.pcpartpicker.db_entities.CPU.PcPartPickerCPUCacheEntity import PcPartPickerCPUCacheEntity
from src.pcpartpicker.db_entities.CPU.PcPartPickerCPUCoreEntity import PcPartPickerCPUCoreEntity
from src.pcpartpicker.db_entities.CPU.PcPartPickerCPUMainDataEntity import PcPartPickerCPUMainDataEntity

from src.pcpartpicker.db_entities.GPU.GPUConnectData import GPUConnectData
from src.pcpartpicker.db_entities.GPU.GPUExternalPower import GPUExternalPowerData
from src.pcpartpicker.db_entities.GPU.GPUMainData import GPUMainData
from src.pcpartpicker.db_entities.GPU.GPUMultiInterface import GPUMultiInterfaceData
from src.pcpartpicker.db_entities.GPU.GPUOutputsData import GPUOutputsData

from src.pcpartpicker.db_entities.Motherboard.MotherboardConnectData import MotherboardConnectData
from src.pcpartpicker.db_entities.Motherboard.MotherboardEthernet import MotherboardEthernet
from src.pcpartpicker.db_entities.Motherboard.MotherboardM2Slots import MotherboardM2Slots
from src.pcpartpicker.db_entities.Motherboard.MotherboardMainData import MotherboardMainData
from src.pcpartpicker.db_entities.Motherboard.MotherboardMemorySpeed import MotherboardMemorySpeed
from src.pcpartpicker.db_entities.Motherboard.MotherboardSocket import MotherboardSocket
from src.pcpartpicker.db_entities.Motherboard.MotherboardMultiInterface import MotherboardMultiInterface

from src.pcpartpicker.db_entities.InternalDrive.HDD import HDD
from src.pcpartpicker.db_entities.InternalDrive.SSD import SSD
from src.pcpartpicker.db_entities.InternalDrive.HybridStorage import HybridStorage

from src.pcpartpicker.db_entities.Case.CaseData import CaseData

from src.pcpartpicker.db_entities.CaseFan.CaseFanData import CaseFanData

from src.pcpartpicker.db_entities.CPUCooler.CPUCoolerData import CPUCoolerData

from src.pcpartpicker.db_entities.PowerSupply.PowerSupplyConnectors import PowerSupplyConnectors
from src.pcpartpicker.db_entities.PowerSupply.PowerSupplyData import PowerSupplyData

color_translations = {
    "Black": "Черный",
    "Yellow": "Желтый",
    "Silver": "Серебристый",
    "White": "Белый",
    "Gray": "Серый",
    "Blue": "Синий",
    "Gold": "Золотой",
    "Red": "Красный",
    "Green": "Зеленый",
    "Platinum": "Платиновый",
    "Orange": "Оранжевый",
    "Camo": "Камуфляж",
    "Multicolor": "Многоцветный",
    "Purple": "Фиолетовый",
    "Pink": "Розовый",
    "Amber": "Янтарный",
    "Beige": "Бежевый",
    "Translucent Blue": "Прозрачно-синий",
    "Transparent": "Прозрачный",
    "Brown": "Коричневый",
    "Clear": "Чистый",
    "Copper": "Медный",
    "Translucent Black": "Прозрачно-черный"
}

class MultiInterface:
    def __init__(self, ways_count, interface_name):
        self.ways_count = ways_count
        self.interface_name = interface_name

@dataclass
class BaseEntity:
    key: str

    def populate_entity(entity, class_name, foreign_column_name):
        my_instance = globals()[class_name]
        db_entity = my_instance()

        for column_name in db_entity.__table__.columns.keys():
            if column_name != "id" and column_name != foreign_column_name:
                setattr(db_entity, column_name, getattr(entity, column_name))

        return db_entity
    
    def handle_value_with_hyphen(self, input_value, replace_value: str):
        if input_value == None:
            return None, None

        values = [float(value.strip()) for value in input_value.replace(replace_value, '').split('-')]

        if len(values) == 1:
            min_value = max_value = values[0]
        elif len(values) == 2:
            min_value, max_value = values
        else:
            raise ValueError("Неверный формат строки!")

        return min_value, max_value

    def translate_colors(self, input_string):
        if input_string != None:
            colors = input_string.split(" / ")
            translated_colors = [color_translations.get(color, color) for color in colors]
            translated_string = " / ".join(translated_colors)

            return translated_string
        else:
            return None
    
    def handle_multi_interface(self, info) -> MultiInterface:
        if info == "CrossFire Capable":
            return MultiInterface(None, "CrossFire")
        
        parts = info.split(' ')

        if parts[1] == 'CrossFire':
            return MultiInterface(int(parts[0].replace('-way', '').replace('-Way', '')), "CrossFire")
        elif parts[1] == 'SLI':
            return MultiInterface(int(parts[0].replace('-way', '').replace('-Way', '')), "SLI")
        else:
            
            return None
        
    def cast_int_fields(self):
        for f in fields(self):
            if f.type == int and isinstance(getattr(self, f.name), str):
                setattr(self, f.name, int(getattr(self, f.name)))

    def cast_float_fields(self):
        for f in fields(self):
            if f.type == float and isinstance(getattr(self, f.name), str):
                setattr(self, f.name, float(getattr(self, f.name)))

    def handle_parameter(self, value, convert_type: type, replace_list: list):
        if value == None or convert_type == None:
            return None
        elif replace_list != None and len(replace_list) != 0:
            handle_value = str(value)
            for string_to_replace in replace_list:
                handle_value = handle_value.replace(string_to_replace, "").replace(" ", "")

        return convert_type(handle_value)
    
    def handle_string_on_na(self, value_string: str):
        if value_string == "N/A":
            return None
        else:
            return value_string

    def handle_price_gb(self, currency_string: str):
        if currency_string != None:
            currency = currency_string[0]
            amount = float(currency_string[1:])

            return currency, amount
        else:
            return None, None

    def handle_parameter_with_measure(self, value, convert_type: type):
        if value == None or convert_type == None:
            return None, None
        else:
            size, unit = str(value).split()
            size.replace(unit, "").replace(" ", "")
            
        return convert_type(size), unit

    def handle_str_none(self, value):
        if value == "None" or value == None:
            return None
        else:
            return str(value)
        
    def handle_fanless(self, value: str):
        if value == "Yes":
            return "No"
        elif value == "No":
            return "Yes"
        else:
            return "No"
    
    def handle_l1_cache(self, value):
        if not value or value == "None":
            return None, None, None, None, None, None

        line_1 = value[0].split(' x ')
        line_2 = value[1].split(' x ')

        return (
            float(line_1[0]), 
            float(line_1[1].split(' ')[0]),
            line_1[1].split(' ')[1],
            float(line_2[0]),
            float(line_2[1].split(' ')[0]), 
            line_2[1].split(' ')[1]
        )

    def handle_l2_l3_cache(self, value):
        if not value or value == "None":
            return None, None, None
        
        cache_spec = value.split(' x ')

        return (
            float(cache_spec[0]),
            float(cache_spec[1].split(' ')[0]),
            cache_spec[1].split(' ')[1]
        )