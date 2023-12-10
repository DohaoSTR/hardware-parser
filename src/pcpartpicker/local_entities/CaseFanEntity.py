from dataclasses import dataclass
import re
from typing import List

from ..BaseEntity import BaseEntity

from ..db_entities.CaseFan.CaseFanData import CaseFanData
from ..db_entities.CaseFan.CaseFanConnector import CaseFanConnector
from ..db_entities.CaseFan.CaseFanFeatures import CaseFanFeatures

@dataclass
class CaseFanEntity(BaseEntity):
    model: str = None
    size: float = None
    color: str = None
    quantity: str = None
    rpm: str = None
    pwm: str = None
    led: str = None

    connector: str = None

    controller: str = None
    static_pressure: str = None
    airflow: str = None
    noise_level: str = None
    bearing_type: str = None

    features: str = None

    min_rpm: float = None
    max_rpm: float = None

    min_airflow: float = None
    max_airflow: float = None

    min_noise_level: float = None
    max_noise_level: float = None

    case_fan: CaseFanData = None
    case_fan_connector: List[CaseFanConnector] = None
    case_fan_features: List[CaseFanFeatures] = None

    def parse_connector_info(self, connector_str):
        connectors = connector_str.split(' + ')

        connector_objects = {}
        index = 0
        for connector in connectors:
            pin_count = 0
            volt_count = 0
            rgb = "No"
            proprietary = "No"
            addressable = "No"
            pwm = "No"

            pin_pattern = r'(\d+)-pin'
            volt_pattern = r'(\d+)V'

            match_pin = re.search(pin_pattern, connector)
            match_volt = re.search(volt_pattern, connector)

            if match_pin:
                pin_count = int(match_pin.group(1))

            if match_volt:
                volt_count = int(match_volt.group(1))

            if "Proprietary" in connector:
                proprietary = "Yes"
            if "RGB" in connector:
                rgb = "Yes"
            if "Addressable" in connector:
                addressable = "Yes"
            if "PWM" in connector:
                pwm = "Yes"

            connector_objects[index] = {
                "pin_count": pin_count,
                "volt_count": volt_count,
                "rgb": rgb,
                "proprietary": proprietary,
                "addressable": addressable,
                "pwm": pwm
            }

            index = index + 1

        return connector_objects

    def __populate_connector(self, value):
        if value == None:
            return None
        
        connector_objects = self.parse_connector_info(value)

        if connector_objects == None:
            return None
        
        entities = []
        for key, object in connector_objects.items():
            pin_count = object["pin_count"]
            volt_count = object["volt_count"]
            rgb = object["rgb"]
            proprietary = object["proprietary"]
            addressable = object["addressable"]
            pwm = object["pwm"]

            entity = CaseFanConnector(pin_count = pin_count, 
                             volt_count = volt_count, 
                             rgb = rgb, 
                             proprietary = proprietary,
                             addressable = addressable,
                             pwm = pwm)
            
            entities.append(entity)

        return entities

    def __populate_features(self, value):
        if isinstance(value, list):
            entities = []
            for item in value:
                entity = CaseFanFeatures(value = item)
                entities.append(entity)
            return entities
        elif isinstance(value, str):
            return [CaseFanFeatures(value = value)]
        else:
            return None

    def __post_init__(self):
        self.size = self.handle_parameter(self.size, float, "mm")
        self.quantity = self.handle_quantity(self.quantity)

        self.min_rpm, self.max_rpm = self.handle_value_with_hyphen(self.rpm, "RPM")

        self.led = self.handle_str_none(self.led)
        self.controller = self.handle_str_none(self.controller)

        self.static_pressure = self.handle_parameter(self.static_pressure, float, "mmH₂O")

        self.min_airflow, self.max_airflow = self.handle_value_with_hyphen(self.airflow, "CFM")
        self.min_noise_level, self.max_noise_level = self.handle_value_with_hyphen(self.noise_level, "dB")

        self.cast_float_fields()
        self.cast_int_fields()

        self.case_fan = self.populate_entity("CaseFanData", "part_id")
        self.case_fan_connector = self.__populate_connector(self.connector)
        self.case_fan_features = self.__populate_features(self.features)

    def handle_quantity(self, value):
        if value == None:
            return None
        elif value == "Single":
            return 1
        elif value == "2-Pack":
            return 2
        elif value == "3-Pack":
            return 3
        elif value == "4-Pack":
            return 4
        elif value == "5-Pack":
            return 5
        elif value == "6-Pack":
            return 6
        else:
            return None