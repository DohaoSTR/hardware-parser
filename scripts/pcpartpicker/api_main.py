import re
from src.pcpartpicker.Part import Part
from src.pcpartpicker.API import API

if __name__ == "__main__":
    data = API.get_unique_values_of_parameter(Part.POWER_SUPPLY, "SpecificationTable", "Output")
    print(data)

    #data = PcPartPickerAPI.get_part_entities_of_all_parts()
