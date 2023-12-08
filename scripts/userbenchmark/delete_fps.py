import json
import os

current_directory = os.getcwd()
current_file_path = current_directory + "\\data\\userbenchmark\\fps_in_games\\" + "gpu_cpu_0_0"
for filename in os.listdir(current_file_path):
    file_path = os.path.join(current_file_path, filename)

    
    # Проверяем, что это файл JSON
    if filename.endswith('.json') and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            data = {key: value for key, value in data.items() if int(key) <= 26000}

            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)

        except json.JSONDecodeError as e:
            print(f"Ошибка при декодировании JSON в файле {filename}: {e}")
        except Exception as e:
            print(f"Произошла ошибка при обработке файла {filename}: {e}")