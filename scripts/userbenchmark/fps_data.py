from src.userbenchmark.mapper.UserBenchmarkAPI import UserBenchmarkAPI

data = UserBenchmarkAPI.get_all_fps_data()
print(len(data))
