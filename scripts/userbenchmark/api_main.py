from src.userbenchmark.Part import Part
from src.userbenchmark.mapper.API import API


#data = API.get_resource(Part.SSD)
#print(data)

#data = API.get_metrics_of_all_parts()
#print(data)

data = API.get_data_of_part(Part.CPU)
print(data)