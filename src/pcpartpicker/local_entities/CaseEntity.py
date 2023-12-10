from dataclasses import dataclass
import re
from typing import List

from ..BaseEntity import BaseEntity

from ..db_entities.Case.CaseFrontPanelUSB import CaseFrontPanelUSB
from ..db_entities.Case.CaseData import CaseData
from ..db_entities.Case.CaseDriveBay import CaseDriveBay
from ..db_entities.Case.CaseExpansionSlot import CaseExpansionSlot
from ..db_entities.Case.CaseMotherboardFormFactor import CaseMotherboardFormFactor

@dataclass
class CaseEntity(BaseEntity):
    type: str = None
    color: str = None
    power_supply: float = None
    side_panel: str = None
    power_supply_shroud: str = None 
    
    front_panel_usb: str = None
    front_panel_usb_entities: List[CaseFrontPanelUSB] = None

    motherboard_form_factor: str = None
    motherboard_form_factor_entities: List[CaseMotherboardFormFactor] = None

    maximum_video_card_length: str = None
    maximum_video_card_length_with: float = None
    maximum_video_card_length_without: float = None

    drive_bays: str = None
    drive_bays_entities: List[CaseDriveBay] = None

    expansion_slots: str = None
    expansion_slots_entities: List[CaseExpansionSlot] = None

    dimensions: str = None
    volume: float = None
    model: str = None
    
    length: float = None
    width: float = None
    height: float = None

    has_power_supply: str = None

    case_data: CaseData = None

    def __populate_front_panel_usb_entities(self, value):
        if isinstance(value, list):
            items = []
            for item in value:
                items.append(CaseFrontPanelUSB(value = item))
            return items
        elif isinstance(value, str):
            return [CaseFrontPanelUSB(value = value)]
        else:
            return None

    def __populate_motherboard_form_factor_entities(self, value):
        if isinstance(value, list):
            items = []
            for item in value:
                items.append(CaseMotherboardFormFactor(value = item))
            return items
        elif isinstance(value, str):
            return [CaseMotherboardFormFactor(value = value)]
        else:
            return None

    def parse_slot_info(self, input_string):
        parts = input_string.rsplit(' x ', 1)
        
        if len(parts) == 2:
            count = int(parts[0])
            rest = parts[1].strip()
            
            if rest.endswith("via Riser"):
                slot_type = rest.replace("via Riser", "").strip()
                via_riser = "Yes"
            else:
                slot_type = rest
                via_riser = "No"
        else:
            return None

        return {'count': count, 'type': slot_type, 'via_riser': via_riser}

    def __populate_expansion_slots_entities(self, value):
        if isinstance(value, list):
            items = []
            for item in value:
                item_data = self.parse_slot_info(item)
                if item_data != None:
                    items.append(CaseExpansionSlot(count = item_data["count"], type = item_data["type"], riser = item_data["via_riser"]))

            return items
        elif isinstance(value, str):
            item_data = self.parse_slot_info(value)
            if item_data != None:
                return [CaseExpansionSlot(count = item_data["count"], type = item_data["type"], riser = item_data["via_riser"])] 
            else:
                return None
        else:
            return None

    def parse_drive_info(self, input_string):
        parts = input_string.split()

        if len(parts) == 4:
            count = int(parts[0])
            location = parts[2].strip()
            drive_type = parts[3].strip().replace('"', '')
        else:
            return None

        return {'count': count, 'location': location, 'drive_type': drive_type}
    
    def __populate_drive_bays_entities(self, value):
        if isinstance(value, list):
            items = []
            for item in value:
                item_data = self.parse_drive_info(item)
                if item_data != None:
                    items.append(CaseDriveBay(count = item_data["count"], type = item_data["location"], format = item_data["drive_type"]))

            return items
        elif isinstance(value, str):
            item_data = self.parse_drive_info(value)
            if item_data != None:
                return [CaseDriveBay(count = item_data["count"], type = item_data["location"], format = item_data["drive_type"])]
            else:
                return None
        else:
            return None

    def __post_init__(self):
        self.power_supply = self.handle_str_none(self.power_supply)
        self.power_supply = self.handle_parameter(self.power_supply, float, "W")

        self.side_panel = self.handle_str_none(self.side_panel)

        self.front_panel_usb = self.handle_list_or_string_on_none(self.front_panel_usb)

        if self.power_supply_shroud != None or self.power_supply != None:
            self.has_power_supply = "Yes"
        else:
            self.has_power_supply = "No"

        self.length, self.width, self.height = self.handle_dimensions(self.dimensions)
        self.volume = self.handle_volume(self.volume)
        self.handle_maximum_video_card_lengths(self.maximum_video_card_length)

        self.cast_float_fields()
        self.cast_int_fields()

        self.case_data = self.populate_entity("CaseData", "part_id")
        self.front_panel_usb_entities = self.__populate_front_panel_usb_entities(self.front_panel_usb)
        self.motherboard_form_factor_entities = self.__populate_motherboard_form_factor_entities(self.motherboard_form_factor)
        self.expansion_slots_entities = self.__populate_expansion_slots_entities(self.expansion_slots)
        self.drive_bays_entities = self.__populate_drive_bays_entities(self.drive_bays)
        
    def handle_list_or_string_on_none(self, value):
        if isinstance(value, list):
            items = []
            for item in value:
                if item == "None":
                    pass
                else:
                    items.append(self.handle_str_none(item))
            return items
        elif isinstance(value, str):
            return self.handle_str_none(value)
        else:
            return None
        
    def handle_volume(self, value):
        if isinstance(value, list):
            return self.handle_parameter(value[0], float, "L")
        elif isinstance(value, str):
            return None
        else:
            return None
        
    def handle_dimensions(self, value):
        if isinstance(value, list):
            values = str(value[0]).split("x")
            return values[0].replace("mm", "").replace(" ", ""), values[1].replace("mm", "").replace(" ", ""), values[2].replace("mm", "").replace(" ", "")
        elif isinstance(value, str):
            return None, None, None
        else:
            return None, None, None

    def handle_maximum_video_card_length(self, value):
        match = re.match(r'([\d.]+)\s*mm\s*/\s*([\d.]+)"\s*(.*)', value)
        
        if match:
            mm_value = float(match.group(1))
            label = match.group(3).strip() if match.group(3) else None
            return {'mm': mm_value, 'label': label}
        else:
            return None

    def handle_maximum_video_card_lengths(self, value):
        if isinstance(value, list):
            for item in value:
                item_data = self.handle_maximum_video_card_length(item)

                if item_data["label"] == "Without Drive Cages":
                    self.maximum_video_card_length_without = item_data["mm"]
                elif item_data["label"] == "With Drive Cages":
                    self.maximum_video_card_length_with = item_data["mm"]
                else:
                    raise Exception("handle_maximum_video_card_lengths - None")           
        elif isinstance(value, str):
            value_data = self.handle_maximum_video_card_length(value)

            if value_data == None:
                print(value)

            if value_data["label"] == "Without Drive Cages":
                self.maximum_video_card_length_without = value_data["mm"]
                self.maximum_video_card_length_with = None
            else:            
                self.maximum_video_card_length_with = value_data["mm"]
                self.maximum_video_card_length_without = None
        else:
            self.maximum_video_card_length_with = None
            self.maximum_video_card_length_without = None