from .TechpowerupWebDriver import TechpowerupWebDriver
from .Part import Part

import logging
from logging import Logger

import json
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import os

GET_PAGE_DATA_MAX_ITERATIONS = 3

class Parameters:
    def __init__(self, logger: Logger = None):
        self.logger = logger or logging.getLogger(__name__)

        self.link = None
        self.web_driver = TechpowerupWebDriver(logger)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.logger is not None:
            self.logger.info(f"Работа парсера завершена, Link: {self.link}")

            self.logger.info("Параметры метода __exit__:")
            self.logger.info(f"Тип возникшего исключения: {exc_type}")
            self.logger.info(f"Значение исключения: {exc_value}")
            self.logger.info(f"Объект traceback: {traceback}")

        self.web_driver.close()
            
        self.logger.info("Вызван метод __exit__, ресурсы очищены.") if self.logger is not None else None

    def __enter__(self):
        return self

    # метод формирующий ссылку на страницу с характеристиками комплектующей
    def __form_part_link(key, part: Part):
        return Part.PART_LINK_MAPPING.get(part) + str(key) 

    # получение типа комплектующей из ссылки
    def __get_part_from_link(self, link):
        parts = link.split("/")

        if len(parts) >= 2:
            last_part = parts[-2].lower()

            for part in Part:
                if last_part.startswith(part.value):
                    return part
                
        return None

    # метод для получения названия комплектующей с страницы
    def __get_part_name_from_html(self, html_content, part: Part):
        soup = BeautifulSoup(html_content, 'html.parser')

        class_name = Part.PART_CLASS_MAPPING.get(part)
        if class_name:
            name_element = soup.find('h1', class_=class_name)
            if name_element:
                return name_element.get_text()

        return None
    
    # метод для получения ключа комплектующей из ссылки
    def __get_key_from_link(self, link):
        parsed = urlparse(link)
        key = parsed.path.split('.')[-1]

        return key

    def __get_main_data(self, html_content, link):
        part_type = self.__get_part_from_link(link)
        part_name = self.__get_part_name_from_html(html_content, part_type)
        key = self.__get_key_from_link(link)

        main_data = []
        main_data.append({ "Header": "Main" })
        main_data.append({ "Name": "PartKey", "Value": key })
        main_data.append({ "Name": "PartName", "Value": part_name })
        main_data.append({ "Name": "PartType", "Value": part_type.value })

        return main_data, part_type
    
    def __get_images_data(self, html_content, part_type: Part):
        soup = BeautifulSoup(html_content, 'html.parser')

        image_links = []
        if part_type == Part.GPU:
            large_links = soup.find_all('a', class_='gpudb-large-image__item')
            for link in large_links:
                image_links.append({ "Name": "LargeImage", "Value": link['href'] })

            item_elements = soup.find_all('div', class_='gpudb-filmstrip__item')
            for item_element in item_elements:
                title_element = item_element.find('div', class_='gpudb-filmstrip__title')
                title = title_element.get_text(strip=True)

                # image с таким title является дубликатом и уже получена в LargeImage
                if title != "GPU":
                    link_element = item_element.find('a', href=True)
                    image_link = link_element['href']
                    
                    image_links.append({ "Name": title, "Value": image_link })
        elif part_type == Part.CPU:
            chip_image_elements = soup.find_all('div', class_='chip-image')
            for chip_image_element in chip_image_elements:
                link_element = chip_image_element.find('a', href=True)

                image_link = None
                if link_element == None:
                    link_element = chip_image_element.find('img')
                    image_link = "https://www.techpowerup.com/" + link_element['src']
                else:
                    image_link = link_element['href']

                title_element = chip_image_element.find('div', class_='chip-image--type')
                title = title_element.get_text(strip=True)

                image_links.append({'Name': title, 'Value': image_link})
        elif part_type == Part.SSD:
            large_links = soup.find_all('a', class_='ssddb-large-image__item')
            for link in large_links:
                image_links.append({ "Name": "LargeImage", "Value": link['href'] })

            item_elements = soup.find_all('div', class_='ssddb-filmstrip__item')
            for item_element in item_elements:
                title_element = item_element.find('div', class_='ssddb-filmstrip__title')
                title = title_element.get_text(strip=True)

                link_element = item_element.find('a', href=True)
                image_link = link_element['href']
                    
                image_links.append({ "Name": title, "Value": image_link })
        
        return image_links

    def __get_recommended_gaming_resolution_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        li_elements = soup.find_all('li', class_='gpudb-recommended-resolutions__entry')
        resolutions = [li.get_text().strip() for li in li_elements]
        section_data = []
        section_data.append({ "Header": "RecommendedGamingResolutions"})
        for resolution in resolutions:
            section_data.append({"Name": "RecommendedGamingResolution", "Value": resolution})

        return section_data

    def __get_notes_data(self, details_section):
        table_data = details_section.find('table').find('td').get_text()
        data_lines = table_data.split("\n")

        data = []
        for line in data_lines:
            parts = line.split(":")
            if len(parts) == 2:
                name = parts[0].strip()
                value = parts[1].strip()
                if value != '':
                    data.append({ "Name": name.replace('\n', '').replace('\t', '').replace('\r', ''), 
                                            "Value": value.replace('\n', '').replace('\t', '').replace('\r', '') })
            else:
                if parts[0] != "\r" and parts[0] != '' and parts[0] != ' ':
                    data.append({ "Name": "Note", "Value": parts[0].replace('\n', '').replace('\t', '').replace('\r', '') })

        return data

    def __get_custom_boards_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        cards = []
        for row in soup.select('table tr'):
            name = row.select_one('.board-table-title__inner a')
            if name:
                name = name.text.strip()
            else:
                continue
                                
            gpu_clock = row.select_one('td:nth-child(2)')
            boost_clock = row.select_one('td:nth-child(3)')
            memory_clock = row.select_one('td:nth-child(4)') 
            other_changes = row.select_one('td:nth-child(5)')

            card = None

            gpu_clock_value = None
            if gpu_clock != None:
                gpu_clock_value = gpu_clock.text
                card = {
                    'name': name,
                    'gpu_clock': gpu_clock_value, 
                }
                                
            boost_clock_value = None
            if boost_clock != None:
                boost_clock_value = boost_clock.text
                card = {
                    'name': name,
                    'gpu_clock': gpu_clock_value, 
                    'boost_clock': boost_clock_value, 
                }

            memory_clock_value = None
            if memory_clock != None:
                memory_clock_value = memory_clock.text
                if memory_clock_value == "":
                    card = {
                        'name': name,
                        'gpu_clock': gpu_clock_value, 
                        'boost_clock': boost_clock_value
                    }
                else:
                    card = {
                        'name': name,
                        'gpu_clock': gpu_clock_value, 
                        'boost_clock': boost_clock_value, 
                        'memory_clock': memory_clock_value
                    }
            
            other_changes_value = None
            if other_changes != None:
                other_changes_value = other_changes.text
                card = {
                    'name': name,
                    'gpu_clock': gpu_clock_value, 
                    'boost_clock': boost_clock_value, 
                    'memory_clock': memory_clock_value,
                    'other_changes': other_changes_value
                }
        
            cards.append(card)

        return cards

    def __get_gpudb_relative_performance_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        cards = []
        for entry in soup.select('.gpudb-relative-performance-entry'):
            name_element = entry.select_one('.gpudb-relative-performance-entry__title')
            percent_element = entry.select_one('.gpudb-relative-performance-entry__number')

            if name_element == None or percent_element == None:
                continue
                                
            name = name_element.text.replace('\n', '').replace('\t', '')
            percent_value = percent_element.text.replace('\n', '').replace('\t', '')

            value = int(percent_value.strip('%'))
            unit_of_measure = percent_value[-1]

            cards.append({'Name': name, 'Value': value, 'UnitOfMeasure': unit_of_measure})

        return cards

    def __get_cpu_ssd_sections_data(self, tr_elements):
        section_data = []
        hardware_versions_list = []

        for tr in tr_elements:
            name_element = tr.find('th')
            value_element = tr.find('td')

            if name_element == None or value_element == None:
                continue

            name = name_element.text.replace('\n', '').replace('\t', '').replace('\r', '')
            value = None

            if name == "Variants:":
                variants = value_element.find_all('span', class_='variants-list--item')

                for variant_item in variants:
                    variant_link = variant_item.a
                    variant_name = None

                    if variant_link:
                        variant_link_value = variant_link['href']
                        variant_link_value = variant_link_value.split('.')[-1]
                        variant_name = variant_link.get_text(strip=True)         
                    else:
                        variant_link_value = None
                        variant_name = variant_item.get_text(strip=True)

                    section_data.append({ "Name": variant_name, "Value": variant_link_value })                                         
            elif name == "Hardware Versions:":
                hardware_versions_list.append({"Header": "Hardware Versions"})
                li_elements_with_style = value_element.find_all('li', style="margin-bottom:5px")

                for li in li_elements_with_style:
                    pattern = r'<li style="margin-bottom:5px">(.*?)<br/>'
                    match = re.search(pattern, str(li), re.DOTALL)
                    header = None
                    if match:
                        header = match.group(1).replace('\n', '').replace('\t', '').replace('\r', '')

                    span_itmes = li.find_all('span')
                    for span in span_itmes:
                        link = span.a
                        if link:
                            link_value = link['href']
                            key_value = link_value.split('.')[-1]
                            capacity = link.get_text(strip=True)
                        else:
                            continue

                        hardware_versions_list.append({'Name': header, 'Capacity': capacity, 'Value': key_value})      
                
                li_elements_display_none = value_element.find('ul', style="display:none").find_all('li')
                for li in li_elements_display_none:
                    link = li.a
                    if link:
                        link_value = link['href']
                        link_value = link_value.split('.')[-1]
                        header = link.get_text(strip=True)
                    else:
                        continue
                    
                    hardware_versions_list.append({'Name': header, 'Value': link_value})                                       
            else:    
                value = value_element.text.replace('\n', '').replace('\t', '').replace('\r', '')
                section_data.append({ "Name": name, "Value": value })

        return section_data, hardware_versions_list

    def __get_gpu_sections_data(self, dl_elements):
        section_data = []
        for dl in dl_elements:
            name_element = dl.find('dt')
            value_element = dl.find('dd')

            if name_element == None or value_element == None:
                continue

            name = name_element.text.replace('\n', '').replace('\t', '').replace('\r', '')   
            value = value_element.text.replace('\n', '').replace('\t', '').replace('\r', '')      

            if name == "Current Price" or name == "Reviews":
                continue

            section_data.append({ "Name": name, "Value": value })

        return section_data                           

    def get_page_data(self, link, max_iteration = GET_PAGE_DATA_MAX_ITERATIONS):
        self.link = link
        current_iteration = 0

        while max_iteration > current_iteration:
            html_content = self.web_driver.get_html_content(link)

            if html_content == None:
                return None
            
            page_data = []
            soup = BeautifulSoup(html_content, 'html.parser')

            main_data, part_type = self.__get_main_data(html_content, link)
            page_data.append(main_data)

            images_links = self.__get_images_data(html_content, part_type)
            images_links.insert(0, { "Header": "Links"})
            page_data.append(images_links)

            # получение RecommendedGamingResolutions для видеокарт
            if part_type == Part.GPU:
                section_data = self.__get_recommended_gaming_resolution_data(html_content)
                page_data.append(section_data)

            hardware_versions_list = []
            sections = soup.find_all('section', class_='details')
            for details_section in sections:
                section_data = []
                if details_section:
                    header = details_section.find('h2')
                    if header == None:
                        header = details_section.find('h1')

                    header_text = None
                    if header != None:
                        header_text = header.text.replace('\n', '').replace('\t', '')
                        
                    if header_text == "Reviews":
                        pass
                    else:
                        section_data.append({ "Header": header_text })

                        if details_section.get('class') == ['details', 'notes']:
                            notes_data = self.__get_notes_data(details_section)
                            section_data.append(notes_data)
                        elif details_section.get('class') == ['details', 'customboards']:
                            self.__get_custom_boards_data(html_content)
                            section_data.append(cards)
                        elif details_section.get('class') == ['details', 'jsonly', 'gpudb-relative-performance']:
                            cards = self.__get_gpudb_relative_performance_data(html_content)
                            section_data.append(cards)
                        else:
                            if part_type == Part.CPU and header_text == "Features":
                                features_list = details_section.find('ul', class_='features')
                                for li in features_list.find_all('li'):
                                    section_data.append({ "Name": "Feature", "Value": li.text })
                            else:
                                tr_elements = details_section.find_all('tr')
                                if tr_elements is not None and len(tr_elements) != 0:
                                    section_data, hardware_versions_list = self.__get_cpu_ssd_sections_data(tr_elements)
                                    page_data.append(section_data)
                                else:
                                    dl_elements = details_section.find_all('dl')
                                    if dl_elements is not None and len(dl_elements) != 0:
                                        section_data = self.__get_gpu_sections_data(dl_elements)
                                        page_data.append(section_data)

                        page_data.append(section_data)
                else:
                    self.logger.warning("details section не найдена.")

            if len(hardware_versions_list) != 0:
                page_data.append(hardware_versions_list)

            return page_data
    
    # метод для получения основных данных о комплектующей по странице
    def __get_header_from_page_data(page_data):
        for section in page_data:
            header = section[0].get("Header", "")
            if header == "Main":
                return section[1:]

    # получение параметров комплектующей
    def get_part_parameters_from_json(part: Part):
        current_file_path = os.path.abspath(__file__)
        file_path = os.path.dirname(current_file_path) + "\\data\\" + str(part.value) + "_parameters.json"
        
        data = None
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                json_file.close()
        except FileNotFoundError:
            return {}

        return data
    
    # сохранение параметров комплеткующей
    def save_part_parameters_to_json(part: Part, data):
        part_parameters = Part.get_part_parameters_from_json(part)

        if part_parameters == {} or len(part_parameters) == 0 or part_parameters == None:
            existing_data = {}
        else:
            existing_data = part_parameters

        existing_data.update(data)

        current_file_path = os.path.abspath(__file__)
        save_directory = os.path.dirname(current_file_path) + "\\data\\"
        filename = part.value + "_parameters"

        with open(save_directory + filename + '.json', 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, indent=4, ensure_ascii=False)
            json_file.close()

    # метод получения последнего ключа из json файла с данными комплектующей
    def get_last_key_of_part(part: Part):
        part_data = Parameters.get_part_parameters_from_json(part)

        if part_data == {}:
            last_key = 0
            return last_key
        
        last_key = list(part_data.keys())[-1]

        return int(last_key)
    
    # проверка на то запаршена ли комплектующая
    # не совсем так работает
    def is_all_parsed(part: Part):
        last_key = Parameters.get_last_key_of_part(part)
        pages_count = Part.PART_PAGES_COUNT_MAPPING.get(part)

        if int(last_key) + 1 == pages_count:
            return True
        else:
            return False
        
    # метод для получения данных о комплектующих конкретного типа
    def get_part_data(self, part: Part, start_index: int = 0):
        pages_data = {}

        for key in range(start_index + 1, Part.PART_PAGES_COUNT_MAPPING.get(part) + 1):
            link = Parameters.__form_part_link(key, part)

            page_data = self.get_page_data(link)
            if(page_data == None):
                self.logger.info(f"{key}. data - комплектующей не существует")
                self.logger.info(f"link - {link}")
                continue

            pages_data[key] = page_data

            self.logger.info(f"{key}. data - {Parameters.__get_header_from_page_data(page_data)}")
            self.logger.info(f"link - {link}")

            if key % 100 == 0:
                Parameters.save_part_parameters_to_json(part, pages_data)

        Parameters.save_part_parameters_to_json(part, pages_data)
        return pages_data

    # метод для получения данных о всех комплектующих
    def get_all_part_data(self):
        for part in Part:
            if Parameters.is_all_parsed(part) == True:
                self.logger.info(f"Part: {part.value}. Все данные получены.")
                continue
            else:
                last_key = Parameters.get_last_key_of_part(part)

                self.logger.info(f"Part: {part.value}. LastKey: {last_key}.")

                if (last_key == 0):
                    start_index = 0
                else:
                    start_index = last_key + 1

                self.get_part_data(part, start_index)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    encoding='utf-8')
    logger = logging.getLogger("techpowerup_parameters")
    file_handler = logging.FileHandler("techpowerup_parser\\logs\\techpowerup_parameters.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    parser = Parameters(logger)
    parser.get_all_part_data()