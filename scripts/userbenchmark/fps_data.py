from src.userbenchmark.mapper.API import API

data = API.get_all_fps_data()
print(len(data))
