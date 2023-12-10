from enum import Enum

class Resolution(Enum):
    HD_720p = "720p"
    FULL_HD_1080p = "1080p"
    QHD_1440p = "1440p"
    ULTRA_HD_4K = "4K"
    NONE = "0"

    def get_part_enum(part_name: str):
        for part in Resolution:
            if part_name == part.value:
                return part
            
        return None
    
    def get_database_value(settings_name: str):
        for settings in Resolution:
            if settings_name == settings.value:
                database_name = Resolution.DATABASE_MAPPING.get(settings)
                return database_name
            
        return None
    
Resolution.DATABASE_MAPPING = {
    Resolution.HD_720p: "720p",
    Resolution.FULL_HD_1080p: "1080p",
    Resolution.QHD_1440p: "1440p",
    Resolution.ULTRA_HD_4K: "4K",
    Resolution.NONE: "None"
}