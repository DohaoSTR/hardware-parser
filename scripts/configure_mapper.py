import time

from src.configure.ConfigureMapper import ConfigureMapper

start_time = time.time()
mapper = ConfigureMapper()
data = mapper.get_compatible_motherboard()
end_time = time.time()
execution_time = end_time - start_time
print(f"Метод выполнился за {execution_time} секунд.")

#print(len(data))
#print(data[0])

#data = ConfigureMapper.get_compatible_parts("RAM")
#print(len(data))