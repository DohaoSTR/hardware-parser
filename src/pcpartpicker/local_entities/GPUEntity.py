from dataclasses import dataclass
import re
from typing import List

from src.pcpartpicker.db_entities.GPU.GPUConnectData import GPUConnectData
from src.pcpartpicker.db_entities.GPU.GPUExternalPower import GPUExternalPowerData
from src.pcpartpicker.db_entities.GPU.GPUMainData import GPUMainData
from src.pcpartpicker.db_entities.GPU.GPUMultiInterface import GPUMultiInterfaceData
from src.pcpartpicker.db_entities.GPU.GPUOutputsData import GPUOutputsData

from ..BaseEntity import BaseEntity, MultiInterface

class PowerInterface:
    def __init__(self, count_external_power, interface_name, pin_count):
        self.count_external_power = count_external_power
        self.interface_name = interface_name
        self.pin_count = pin_count

@dataclass
class GPUEntity(BaseEntity):
    model: str = None
    chipset: str = None
    memory: float = None
    memory_type: str = None
    core_clock: int = None
    boost_clock: int = None
    effective_memory_clock: int = None
    interface: str = None
    color: str = None
    frame_sync: str = None
    length: int = None
    tdp: int = None
    case_expansion_slot_width: int = None
    total_slot_width: int = None

    hdmi_outputs: int = None
    displayport_outputs: int = None
    hdmi_2_1a_outputs: int = None
    displayport_1_4_outputs: int = None
    displayport_1_4a_outputs: int = None
    dvi_d_dual_link_outputs: int = None
    hdmi_2_1_outputs: int = None
    displayport_2_1_outputs: int = None
    displayport_2_0_outputs: int = None
    hdmi_2_0b_outputs: int = None
    dvi_i_dual_link_outputs: int = None
    usb_type_c_outputs: int = None
    vga_outputs: int = None
    virtuallink_outputs: int = None
    dvi_d_single_link_outputs: int = None
    minidisplayport_2_1_outputs: int = None
    hdmi_2_0_outputs: int = None
    dvi_outputs: int = None
    minidisplayport_outputs: int = None
    hdmi_1_4_outputs: int = None
    minidisplayport_1_4a_outputs: int = None
    minidisplayport_1_4_outputs: int = None
    vhdci_outputs: int = None
    dvi_i_single_link_outputs: int = None
    s_video_outputs: int = None
    mini_hdmi_outputs: int = None
    displayport_1_3_outputs: int = None
    dvi_a_outputs: int = None

    cooling: str = None
    external_power: str = None
    multi_interface: list = None

    radiator_mm: int = None
    fans_count: int = None

    power_interface_1: PowerInterface = None
    power_interface_2: PowerInterface = None

    multi_interfaces: List[MultiInterface] = None

    main_data: GPUMainData = None 
    outputs_data: GPUOutputsData = None
    multi_interface_data: List[GPUMultiInterfaceData] = None
    external_power_data_1: GPUExternalPowerData = None
    external_power_data_2: GPUExternalPowerData = None
    connect_data: GPUConnectData = None
    
    def __populate_external_power_entity(self, power_interface: PowerInterface):
        if power_interface == None:
            return None
        else:
            db_entity = GPUExternalPowerData(interface_name = power_interface.interface_name, 
                                            interface_count = power_interface.count_external_power, 
                                            pin_count = power_interface.pin_count)
            
            return db_entity
        
    def __populate_multi_interface_entities(self, multi_interfaces: List[MultiInterface]):
        multi_interface_data: List[GPUMultiInterfaceData] = []

        if multi_interfaces != None:
            for interface in multi_interfaces:
                db_entity = GPUMultiInterfaceData(ways_count = interface.ways_count, name_technology = interface.interface_name)
                multi_interface_data.append(db_entity)

        return multi_interface_data

    def __post_init__(self):
        self.core_clock = self.handle_parameter(self.core_clock, int, "MHz")
        self.boost_clock = self.handle_parameter(self.boost_clock, int, "MHz")
        self.effective_memory_clock = self.handle_parameter(self.effective_memory_clock, int, "MHz")

        self.memory = self.handle_parameter(self.effective_memory_clock, float, "GB")

        self.length = self.handle_parameter(self.length, int, "mm")
        self.frame_sync = self.handle_str_none(self.frame_sync)
        self.tdp = self.handle_parameter(self.tdp, int, "W")

        self.radiator_mm, self.fans_count = self.handle_cooling(self.cooling)
        self.power_interface_1, self.power_interface_2 = self.handle_external_power(self.external_power)

        if self.multi_interface != None:
            self.multi_interfaces = []

            if type(self.multi_interface) == list:
                for interface in self.multi_interface:
                    self.multi_interfaces.append(self.handle_multi_interface(interface))
            elif type(self.multi_interface) == str:
                self.multi_interfaces.append(self.handle_multi_interface(self.multi_interface))

        self.cast_int_fields()

        self.main_data = self.populate_entity("GPUMainData", "part_id")
        self.outputs_data = self.populate_entity("GPUOutputsData", "part_id")
        self.connect_data = self.populate_entity("GPUConnectData", "part_id")
        self.external_power_data_1 = self.__populate_external_power_entity(self.power_interface_1)
        self.external_power_data_2 = self.__populate_external_power_entity(self.power_interface_2)
        self.multi_interface_data = self.__populate_multi_interface_entities(self.multi_interfaces)

    def handle_external_power(self, line) -> PowerInterface:
        parts = line.split(' ')

        if len(parts) == 3:
            count_external_power = int(parts[0])
            interface_name = parts[1]
            pin_count = int(parts[2].replace("-pin", ""))
            return PowerInterface(count_external_power, interface_name, pin_count), None
        elif len(parts) == 1 and parts[0] == "None":
            return None, None
        elif len(parts) == 7:
            count_external_power_1 = int(parts[0])
            interface_name_1 = parts[1]
            pin_count_1 = int(parts[2].replace("-pin", ""))

            count_external_power_2 = int(parts[4])
            interface_name_2 = parts[5]
            pin_count_2 = int(parts[6].replace("-pin", ""))
            return PowerInterface(count_external_power_1, interface_name_1, pin_count_1), PowerInterface(count_external_power_2, interface_name_2, pin_count_2)
        else:
            raise ValueError(f"Invalid power line format: {line}")

    def handle_cooling(self, value):
        if value == None and value == "Fanless":
            return None, None
        else:
            match = re.search(r'(\d+) mm Radiator', value)
            radiator_mm = int(match.group(1)) if match else None

            match = re.search(r'(\d+) Fans', value)
            fans_count = int(match.group(1)) if match else None

            return radiator_mm, fans_count