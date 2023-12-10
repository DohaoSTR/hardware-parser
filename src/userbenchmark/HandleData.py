from .Part import Part
from .PartMetrics import PartMetrics
from .AsyncFPSData import AsyncFPSData
from .GameKeys import GameKeys
from .PartKeys import PartKeys
from .KeysHandling import KeysHandling

# получение всех игровых ключей
def get_game_keys(games_value):
    game_keys = GameKeys.get_game_keys_from_json()
    game_keys_list = list(game_keys.keys())
    games = game_keys_list[:games_value]
    
    return games

# удаление повторений из ключей
def remove_duplicates_part_keys(part: Part):
    data = PartKeys.get_part_keys_from_json(part)

    unique_keys = {}
    handled_data = {}

    for key, value in data.items():
        key_value = value["key"]
        if key_value not in unique_keys:
            unique_keys[key_value] = True
            handled_data[key] = value

    return handled_data

# удаление всех ключей из папки где, количество samples низкое
# переделать так чтобы еще сохранялась model и был тот же формат
def remove_keys_with_small_sum(fps_data, part: Part, min_samples_sum):
    sum_samples = {}
    key_name = part.value + "_key"

    for key, value in fps_data.items():
        cpu_key = value[key_name]
        samples_value = value['samples_value']
        if cpu_key in sum_samples:
            sum_samples[cpu_key] += samples_value
        else:
            sum_samples[cpu_key] = samples_value

    filtered_sum_samples = {key: value for key, value in sum_samples.items() if value >= min_samples_sum}
    sum_samples = filtered_sum_samples

    return sum_samples

# сохранение отфильтрованных ключей
def get_handled_data(part: Part):
    name_folder = part.value + "_0_0"
    fps_data = AsyncFPSData.get_fps_in_games_data(name_folder)
    sum_samples = remove_keys_with_small_sum(fps_data, part, 200)
    handled_data = remove_duplicates_part_keys(part)
    filtered_data = {key: value for key, value in handled_data.items() if int(value['key']) in sum_samples}

    return filtered_data

# проверка на полное соответствие названий метрик
def check_compability_names():
    for part in Part:
        data = PartMetrics.get_metric_names_from_json(part)
        last_inner_key = None
        for key, value in data.items():
            for inner_key, inner_value in value.items():
                if inner_key == "key":
                    last_inner_key = inner_value
                else:
                    if inner_value == "Gaming" or inner_value == "Desktop" or inner_value == "Workstation":
                        pass
                    else:
                        print(last_inner_key)


if __name__ == "__main__":
    for part in Part:      
       data = remove_duplicates_part_keys(part)
       KeysHandling.save_part_keys_without_duplicates_to_json(part, data)

    handled_data =  get_handled_data(Part.CPU)
    KeysHandling.save_handled_fps_keys_to_json(Part.CPU, handled_data)

    handled_data =  get_handled_data(Part.GPU)
    KeysHandling.save_handled_fps_keys_to_json(Part.GPU, handled_data)

    check_compability_names()