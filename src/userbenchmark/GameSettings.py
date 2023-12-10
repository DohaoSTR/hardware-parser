from enum import Enum

class GameSettings(Enum):
    LOW = "Low"
    MED = "Med"
    HIGH = "High"
    MAX = "Max"
    NONE = "0"

    def get_part_enum(part_name: str):
        for part in GameSettings:
            if part_name == part.value:
                return part
            
        return None
    
    def get_database_value(settings_name: str):
        for settings in GameSettings:
            if settings_name == settings.value:
                database_name = GameSettings.DATABASE_MAPPING.get(settings)
                return database_name
            
        return None
    
GameSettings.DATABASE_MAPPING = {
    GameSettings.LOW: "Low",
    GameSettings.MED: "Med",
    GameSettings.HIGH: "High",
    GameSettings.MAX: "Max",
    GameSettings.NONE: "None"
}