import time

from src.configure.ConfigureModel import ConfigureModel, MetricCalculationType

def execute_model():
    start_time = time.time()
    model = ConfigureModel()
    combinations = model.parse_all_combinations_of_main_configure()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Метод выполнился за {execution_time} секунд.")

    print(len(combinations))

    model.save_all_combinations(combinations)

def test():
    start_time = time.time()
    model = ConfigureModel()
    data = model.pick_up_main_configure(MetricCalculationType.AVERAGE)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Метод выполнился за {execution_time} секунд.")
    
    for item in data:
        print(f"Metric - {item.part_metric}, CPU id - {item.cpu_id}, GPU id - {item.gpu_id}, RAM id - {item.ram_id}")

#execute_model()
test()