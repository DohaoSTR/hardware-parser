from dataclasses import dataclass
import re
from typing import List

from ..BaseEntity import BaseEntity

from ..db_entities.PowerSupply.PowerSupplyConnectors import PowerSupplyConnectors
from ..db_entities.PowerSupply.PowerSupplyData import PowerSupplyData
from ..db_entities.PowerSupply.PowerSupplyEfficiency import PowerSupplyEfficiency
from ..db_entities.PowerSupply.PowerSupplyOutput import PowerSupplyOutput

@dataclass
class PcPartPickerPowerSupplyEntity(BaseEntity):
    model: str = None
    type: str = None
    efficiency_rating: str = None
    wattage: float = None
    length: float = None
    modular: str = None
    color: str = None
    fanless: str = None

    atx_4pin_connectors: int = None
    eps_8pin_connectors: int = None
    pcie_12_4pin_12vhpwr_connectors: int = None
    pcie_12pin_connectors: int = None
    pcie_8pin_connectors: int = None
    pcie_6_2pin_connectors: int = None
    pcie_6pin_connectors: int = None
    sata_connectors: int = None
    molex_4pin_connectors: int = None

    efficiency: str = None
    output: str = None

    fan: str = None

    power_supply: PowerSupplyData = None
    power_supply_connectors: PowerSupplyConnectors = None
    power_supply_efficiency: List[PowerSupplyEfficiency] = None
    power_supply_outputs: List[PowerSupplyOutput] = None

    def __populate_efficiency(self, value: str):
        if value != None:
            if value.__contains__("</br>"):
                values = value.split("</br>")
                items = []
                for item in values:
                    items.append(PowerSupplyEfficiency(value = item))
                return items
            else:
                if value != None:
                    return [PowerSupplyEfficiency(value = value)]
                else: 
                    return None
        else:
            return None

    def parse_power_line(self, line: str):
        power_match = re.search(r'(\d+W)', line)
        combined_match = re.search(r'Combined', line)
        description_match = re.search(r'\((.*?)\)', line)

        if line.__contains__("A@"):
            voltage_match = re.search(r'@((\+|-| \+ | - )?(\d+)?(?:\.\d+)?.*)', line, re.IGNORECASE)
            current_match = re.search(r'(\d+(?:\.\d+)?A)@', line)
        else:
            voltage_match = re.search(r'((\+|-| \+ | - )?(\d+)?(?:\.\d+)?.*@)', line, re.IGNORECASE)
            current_match = re.search(r'@(\d+(?:\.\d+)?A)', line)

        dc_mode = 'No'
        if line.__contains__("DC"):
            dc_mode = 'Yes'
            
        voltage_mode = voltage_match.group(1) if voltage_match else None
        ampere = current_match.group(1) if current_match else None
        power = power_match.group(1) if power_match and current_match is None else None
        combined = 'Yes' if combined_match else 'No' if combined_match is not None else 'No'
        description = description_match.group(1) if description_match else None

        if line == " +3.3A@30A":
            voltage_mode = "+3.3V"
            ampere = "30"

        if combined is not None and voltage_mode is not None:    
            voltage_mode.replace("Combined", "")

        if voltage_mode is not None:
            voltage_mode = voltage_mode.replace("@", "").replace("DC Standby", "").replace("DC", "").replace(" ", "")

        if ampere is not None:
            ampere = float(ampere.replace("A", ""))

        if power is not None:
            power = float(power.replace("W", ""))

        return {
                "voltage_mode": voltage_mode,
                "ampere": ampere,
                "power": power,
                "combined": combined,
                "dc_mode": dc_mode,
                "description": description
            }

    def parse_comma_line(self, value):
        values = re.split(r'<br/>', value)

        items = []
        for item in values:
            elements = re.split(r',', item)

            voltage_mode = elements[0].replace(" ", "")
            ampere = elements[1].replace(" ", "").replace("A", " ")
            power = elements[2].replace(" ", "").replace("W", " ")
            combined = "No"
            description = None
            dc_mode = "No"

            entity = PowerSupplyOutput(voltage_mode = voltage_mode, 
                        ampere = ampere, 
                        power = power, 
                        combined = combined, 
                        description = description,
                        dc_mode = dc_mode)
            items.append(entity)

        return items  

    def __populate_output(self, value):
        if value == "+3.3V, 20A, 110W<br/>+5V, 20A, 110W<br/>+12V, 20A, 750W<br/>+12V, 20A, 750W<br/>+12V, 30A, 750W<br/>+12V, 30A, 750W<br/>-12V, 0.5A, 6W<br/>+5VSB, 3A, 15W":
            return self.parse_comma_line(value)

        if value != None:
            if str(value).__contains__("combined"):
                values = re.split(r'<br/>|</br>|;', value)
            else:
                values = re.split(r'<br/>|,|</br>|;', value)

            if value.__contains__("A@") and value != "+3.3A@30A":
                values = re.split(r',', value)

            if str(value).__contains__("+5V@30A (+3.3V ; +5V = 150W max.)"):
                values = re.split(r',', value)

            if str(value).__contains__("DC Standby"):
                new_values = []
                for item in values:
                    if item != None:
                        new_values.append(item.replace(" ", ""))
                values = new_values

            items = []
            for item in values:
                object = self.parse_power_line(item)
                voltage_mode = object["voltage_mode"]
                ampere = object["ampere"]
                power = object["power"]
                combined = object["combined"]
                description = object["description"]
                dc_mode = object["dc_mode"]

                if voltage_mode is None and ampere is None and power is None and (combined is None or "No") and description is None and (dc_mode is None or "No"):
                    pass
                else:
                    entity = PowerSupplyOutput(voltage_mode = voltage_mode, 
                                            ampere = ampere, 
                                            power = power, 
                                            combined = combined, 
                                            description = description,
                                            dc_mode = dc_mode)
                    items.append(entity)
            return items
        else:
            return None

    def __post_init__(self):
        self.wattage = self.handle_parameter(self.wattage, float, "W")
        self.length = self.handle_parameter(self.length, float, "mm")

        self.fan = self.handle_fanless(self.fanless)

        self.cast_float_fields()
        self.cast_int_fields()

        self.power_supply = self.populate_entity("PowerSupplyData", "part_id")
        self.power_supply_connectors = self.populate_entity("PowerSupplyConnectors", "power_supply_id")
        self.power_supply_efficiency = self.__populate_efficiency(self.efficiency)

        self.power_supply_outputs = self.__populate_output(self.output)