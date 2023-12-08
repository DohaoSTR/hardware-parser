from src.userbenchmark.UserBenchmarkPart import UserBenchmarkPart
from src.userbenchmark.mapper.UserBenchmarkAPI import UserBenchmarkAPI


#data = UserBenchmarkAPI.get_resource(UserBenchmarkPart.SSD)
#print(data)

#data = UserBenchmarkAPI.get_metrics_of_all_parts()
#print(data)

data = UserBenchmarkAPI.get_data_of_part(UserBenchmarkPart.CPU)
print(data)