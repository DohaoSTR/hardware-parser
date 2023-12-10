from dataclasses import dataclass
import re
from typing import List

from ..db_entities.Motherboard.MotherboardEthernet import MotherboardEthernet
from ..db_entities.Motherboard.MotherboardM2Slots import MotherboardM2Slots
from ..db_entities.Motherboard.MotherboardMainData import MotherboardMainData
from ..db_entities.Motherboard.MotherboardMemorySpeed import MotherboardMemorySpeed
from ..db_entities.Motherboard.MotherboardMultiInterface import MotherboardMultiInterface
from ..db_entities.Motherboard.MotherboardSocket import MotherboardSocket
from ..db_entities.Motherboard.MotherboardConnectData import MotherboardConnectData

from ..BaseEntity import BaseEntity, MultiInterface

@dataclass
class MotherboardEntity(BaseEntity):
    socket: str = None
    memory_speed: str = None
    m2_slots: str = None
    multi_interface: str = None
    onboard_ethernet: str = None

    form_factor: str = None
    chipset: str = None
    memory_max: int = None
    memory_type: str = None
    memory_slots: int = None
    color: str = None

    pcie_x16_slots: int = None
    pcie_x8_slots: int = None
    pcie_x4_slots: int = None
    pcie_x1_slots: int = None
    pci_slots: int = None

    mini_pcie_slots: int = None
    half_mini_pcie_slots: int = None
    mini_pcie_msata_slots: int = None
    msata_slots: int = None
    sata_6_0: int = None

    onboard_video: str = None

    usb_2_0_headers: int = None
    usb_2_0_headers_single_port: int = None
    usb_3_2_gen_1_headers: int = None
    usb_3_2_gen_2_headers: int = None
    usb_3_2_gen_2x2_headers: int = None

    supports_ecc: str = None
    raid_support: str = None
    model: str = None

    pata_100: int = None
    sata_3_0: int = None
    esata_6_0: int = None
    u_2: int = None
    esata_3_0: int = None
    sas_3_0: int = None
    pata_133: int = None
    sas_12_0: int = None
    sas_6_0: int = None
    sata_1_5: int = None
    
    multi_interfaces: List[MultiInterface] = None

    wireless_networking: str = None 
    wifi_standard: str = None
    network_adapter_speed: float = None

    socket_entities: List[MotherboardSocket] = None
    ethernet_entities: List[MotherboardEthernet] = None
    memory_speed_entites: List[MotherboardMemorySpeed] = None
    interface_entities: List[MotherboardMultiInterface] = None
    m2_entities: List[MotherboardM2Slots] = None

    main_data: MotherboardMainData = None
    connect_data: MotherboardConnectData = None

    def __populate_socket_entities(self):
        self.socket_entities = []
        match = re.search(r"(\d+)\s*x\s*(\w+)", self.socket)

        if match:
            count = int(match.group(1))
            socket = match.group(2)
            self.socket_entities.append(MotherboardSocket(socket_count = count, socket_name = socket))
        elif '/' in self.socket:
            sockets = self.socket.split('/')
            self.socket_entities.append(MotherboardSocket(socket_count = 1, socket_name = sockets[0]))
            self.socket_entities.append(MotherboardSocket(socket_count = 1, socket_name = sockets[1]))
        else:
            self.socket_entities.append(MotherboardSocket(socket_count = 1, socket_name = self.socket))

    def parse_network_string(self, network_string):
        speed_match = re.search(r'(\d+) x (.+) (..)/s', network_string)
        if speed_match:
            count = int(speed_match.group(1))
            speed = float(speed_match.group(2))
            speed_measure = speed_match.group(3) + "/s"

            adapter_match = re.search(r'(\d+(?:\.\d+)?) (..)/s \((.+)\)', network_string)
            
            if adapter_match != None:
                adapter = adapter_match.group(3)
            else:
                adapter = None

            adapter_match

            network_info = {
            "network_adapter_count": count,
            "network_adapter_speed": speed, 
            "speed_measure":  speed_measure,
            "network_adapter":  adapter
            }
            
            return network_info
        else:
            return None

    def parse_network_info(self, network_list):
        if isinstance(network_list, list):
            data = []
            for sub_item in network_list:
                network_string = self.parse_network_string(sub_item)
                data.append(network_string)
            return data
        else:
            if network_list != None:
                return self.parse_network_string(network_list)
            else:
                return None

    def __populate_ethernet_entities(self):
        self.ethernet_entities = []

        network_info = self.parse_network_info(self.onboard_ethernet)

        if network_info != None:
            if isinstance(network_info, list):
                for item in network_info:
                    count = item["network_adapter_count"]
                    speed = item["network_adapter_speed"]
                    meausure = item["speed_measure"]
                    adapter = item["network_adapter"]

                    self.ethernet_entities.append(MotherboardEthernet(network_adapter_count = count, network_adapter_speed = speed, 
                                                                    speed_measure = meausure, network_adapter = adapter))
            else:
                count = network_info["network_adapter_count"]
                speed = network_info["network_adapter_speed"]
                meausure = network_info["speed_measure"]
                adapter = network_info["network_adapter"]
                self.ethernet_entities.append(MotherboardEthernet(network_adapter_count = count, network_adapter_speed = speed, 
                                                                    speed_measure = meausure, network_adapter = adapter))

    def __populate_memory_speed_entites(self):
        self.memory_speed_entites = []
        if isinstance(self.memory_speed, list):
            for item in self.memory_speed:
                memory_type = item.split("-")[0]
                memory_speed = item.split("-")[1]
                self.memory_speed_entites.append(MotherboardMemorySpeed(memory_type = memory_type, memory_speed = memory_speed))
        else:
            memory_type = self.memory_speed.split("-")[0]
            memory_speed = self.memory_speed.split("-")[1]
            self.memory_speed_entites.append(MotherboardMemorySpeed(memory_type = memory_type, memory_speed = memory_speed))

    def __populate_interface_entities(self):
        self.interface_entities = []

        if self.multi_interfaces != None:
            for interface in self.multi_interfaces:
                db_entity = MotherboardMultiInterface(ways_count = interface.ways_count, name_technology = interface.interface_name)
                self.interface_entities.append(db_entity)

    def parse_key_specification(self, input_str: str):
        numbers = re.findall(r'\d+', input_str)
        keys = re.findall(r'[A-Z]-key', input_str)
        description = re.search(r'\((.*)\)', input_str)
        if description:
            description = description.group(1)

        return numbers, keys[0], description

    def __populate_m2_entities(self):
        self.m2_entities = []
        if self.m2_slots != None:
            if isinstance(self.m2_slots, list):
                for item in self.m2_slots:
                    numbers, key, description = self.parse_key_specification(item)
                    for number in numbers:
                        entity = MotherboardM2Slots(standard_size = number, key_name = key, description = description)
                        self.m2_entities.append(entity)
            else:
                numbers, key, description = self.parse_key_specification(self.m2_slots)
                for number in numbers:
                    entity = MotherboardM2Slots(standard_size = number, key_name = key, description = description)
                    self.m2_entities.append(entity)
    
    def __post_init__(self):
        if self.multi_interface != None:
            self.multi_interfaces = []
            if type(self.multi_interface) == list:
                for interface in self.multi_interface:
                    self.multi_interfaces.append(self.handle_multi_interface(interface))
            elif type(self.multi_interface) == str:
                self.multi_interfaces.append(self.handle_multi_interface(self.multi_interface))

        self.memory_max = self.handle_parameter(self.memory_max, int, "GB")

        self.wifi_standard, self.network_adapter_speed = self.handle_wireless_networking(self.wireless_networking)

        self.cast_float_fields()
        self.cast_int_fields()

        self.__populate_socket_entities()
        self.__populate_ethernet_entities()
        self.__populate_memory_speed_entites()
        self.__populate_interface_entities()
        self.__populate_m2_entities()

        self.main_data = self.populate_entity("MotherboardMainData", "part_id")
        self.connect_data = self.populate_entity("MotherboardConnectData", "motherboard_id")

    def handle_wireless_networking(self, wifi_string):
        match = re.match(r"Wi-Fi (.+)", wifi_string)

        if match:
            if match.group(1).__contains__("GHz"):
                ghz_match = re.match(r"Wi-Fi\s+(.+)\((\d+(?:\.\d+)?)", wifi_string)
                wifi_version = ghz_match.group(1)
                wifi_speed = float(ghz_match.group(2))
            else:
                wifi_version = match.group(1)
                wifi_speed = None

            return wifi_version, wifi_speed
        else:
            return None, None