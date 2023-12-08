import re
from src.pcpartpicker.PcPartPickerPart import PcPartPickerPart
from src.pcpartpicker.PcPartPickerAPI import PcPartPickerAPI

if __name__ == "__main__":
    data = PcPartPickerAPI.get_unique_values_of_parameter(PcPartPickerPart.POWER_SUPPLY, "SpecificationTable", "Output")
    print(data)

    #data = PcPartPickerAPI.get_part_entities_of_all_parts()
