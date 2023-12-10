from enum import Enum

class UserBenchmarkResolution(Enum):
    HD_720p = "720p"
    FULL_HD_1080p = "1080p"
    QHD_1440p = "1440p"
    ULTRA_HD_4K = "4K"
    NONE = "0"

    def get_part_enum(part_name: str):
        for part in UserBenchmarkResolution:
            if part_name == part.value:
                return part
            
        return None
    
    def get_database_value(settings_name: str):
        for settings in UserBenchmarkResolution:
            if settings_name == settings.value:
                database_name = UserBenchmarkResolution.DATABASE_MAPPING.get(settings)
                return database_name
            
        return None
    
UserBenchmarkResolution.DATABASE_MAPPING = {
    UserBenchmarkResolution.HD_720p: "720p",
    UserBenchmarkResolution.FULL_HD_1080p: "1080p",
    UserBenchmarkResolution.QHD_1440p: "1440p",
    UserBenchmarkResolution.ULTRA_HD_4K: "4K",
    UserBenchmarkResolution.NONE: "None"
}