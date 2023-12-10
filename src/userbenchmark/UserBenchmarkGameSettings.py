from enum import Enum

class UserBenchmarkGameSettings(Enum):
    LOW = "Low"
    MED = "Med"
    HIGH = "High"
    MAX = "Max"
    NONE = "0"

    def get_part_enum(part_name: str):
        for part in UserBenchmarkGameSettings:
            if part_name == part.value:
                return part
            
        return None
    
    def get_database_value(settings_name: str):
        for settings in UserBenchmarkGameSettings:
            if settings_name == settings.value:
                database_name = UserBenchmarkGameSettings.DATABASE_MAPPING.get(settings)
                return database_name
            
        return None
    
UserBenchmarkGameSettings.DATABASE_MAPPING = {
    UserBenchmarkGameSettings.LOW: "Low",
    UserBenchmarkGameSettings.MED: "Med",
    UserBenchmarkGameSettings.HIGH: "High",
    UserBenchmarkGameSettings.MAX: "Max",
    UserBenchmarkGameSettings.NONE: "None"
}