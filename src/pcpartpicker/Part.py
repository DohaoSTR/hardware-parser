from enum import Enum

# кол-во страниц для каждой категории
CPU_PAGES = 14
CPU_COOLERS_PAGES = 22
MOTHEBOARDS_PAGES = 44
MEMORY_PAGES = 117
STORAGES_PAGES = 57
VIDEO_CARDS_PAGES = 58
POWER_SUPPLIES_PAGES = 28
CASES_PAGES = 55

CASE_FAN_PAGES = 22
UPS_PAGES = 7
OPTICAL_DRIVE_PAGES = 3
EXTERNAL_STORAGE_PAGES = 6
FAN_CONTROLLER_PAGES = 1
THERMAL_PASTE_PAGES = 2

SOUND_CARD_PAGES = 1
WIRED_NETWORK_CARD_PAGES = 2
WIRELESS_NETWORK_CARD_PAGES = 4

OPERATING_SYSTEM_PAGES = 1
MONITOR_PAGES = 42

HEADPHONES_PAGES = 28
KEYBOARD_PAGES = 29
MOUSE_PAGES = 24
SPEAKERS_PAGES = 3
WEBCAM_PAGES = 1


# перечисление для категорий комплектующих
# CPU = ["cpu", CPU_PAGES]
# "cpu" - название категории используемое сайтом в ссылках
# CPU_PAGES - кол-во страниц для каждой категории
class Part(Enum):
    CPU = "cpu"
    CPU_COOLER = "cpu-cooler"
    MOTHEBOARD = "motherboard"
    MEMORY = "memory"
    STORAGE = "internal-hard-drive"
    VIDEO_CARD = "video-card"
    POWER_SUPPLY = "power-supply"
    CASE = "case"

    CASE_FAN = "case-fan"
    UPS = "ups"
    OPTICAL_DRIVE = "optical-drive"
    EXTERNAL_STORAGE = "external-hard-drive"
    FAN_CONTROLLER = "fan-controller"
    THERMAL_PASTE = "thermal-paste"
    
    SOUND_CARD = "sound-card"
    WIRED_NETWORK_CARD = "wired-network-card"
    WIRELESS_NETWORK_CARD = "wireless-network-card"

    MONITOR = "monitor"
    OPERATING_SYSTEM = "os"

    HEADPHONES = "headphones"
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    SPEAKERS = "speakers"
    WEBCAM = "webcam"

    def get_part_enum(part_name: str):
        for part in Part:
            if part_name == part.value:
                return part
            
        return None
    
    def get_pages_count(part_name: str):
        for part in Part:
            if part_name == part.value:
                pages_count = Part.PAGES_COUNT_MAPPING.get(part)
                return pages_count
            
        return None

Part.PAGES_COUNT_MAPPING = {
    Part.CPU: CPU_PAGES,
    Part.CPU_COOLER: CPU_COOLERS_PAGES,
    Part.MOTHEBOARD: MOTHEBOARDS_PAGES,
    Part.MEMORY: MEMORY_PAGES,
    Part.STORAGE: STORAGES_PAGES,
    Part.VIDEO_CARD: VIDEO_CARDS_PAGES,
    Part.POWER_SUPPLY: POWER_SUPPLIES_PAGES,
    Part.CASE: CASES_PAGES,
    Part.CASE_FAN: CASE_FAN_PAGES,
    Part.UPS: UPS_PAGES,
    Part.OPTICAL_DRIVE: OPTICAL_DRIVE_PAGES,
    Part.EXTERNAL_STORAGE: EXTERNAL_STORAGE_PAGES,
    Part.FAN_CONTROLLER: FAN_CONTROLLER_PAGES,
    Part.THERMAL_PASTE: THERMAL_PASTE_PAGES,
    Part.SOUND_CARD: SOUND_CARD_PAGES,
    Part.WIRED_NETWORK_CARD: WIRED_NETWORK_CARD_PAGES,
    Part.WIRELESS_NETWORK_CARD: WIRELESS_NETWORK_CARD_PAGES,
    Part.MONITOR: MONITOR_PAGES,
    Part.OPERATING_SYSTEM: OPERATING_SYSTEM_PAGES,
    Part.HEADPHONES: HEADPHONES_PAGES,
    Part.KEYBOARD: KEYBOARD_PAGES,
    Part.MOUSE: MOUSE_PAGES,
    Part.SPEAKERS: SPEAKERS_PAGES,
    Part.WEBCAM: WEBCAM_PAGES,
}