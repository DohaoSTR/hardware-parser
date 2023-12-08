from enum import Enum

CPU_PAGES_COUNT = 3500
GPU_PAGES_COUNT = 4300
SSD_PAGES_COUNT = 1800

CPU_UNIQUE_LINK = "https://www.techpowerup.com/cpu-specs/core-i9-14900k.c"
GPU_UNIQUE_LINK = "https://www.techpowerup.com/gpu-specs/geforce-rtx-4090.c"
SSD_UNIQUE_LINK = "https://www.techpowerup.com/ssd-specs/samsung-970-evo-plus-1-tb.d"

# перечесление категорий комплектуюших на сайте Techpowerup
# CPU = "CPU"
# "CPU" - значение используемое для обозначение категории
# при сохранении характеристик комплектующих
class TechpowerupPart(Enum):
    CPU = 'cpu'
    GPU = 'gpu'
    SSD = 'ssd'

    def get_part_enum(part_name: str):
        for part in TechpowerupPart:
            if part_name == part.value:
                return part
            
        return None
    
    def get_part_link(self):
        for part in TechpowerupPart:
            if self == part:
                return part
            
        return None


TechpowerupPart.PART_LINK_MAPPING = {
    TechpowerupPart.CPU: CPU_UNIQUE_LINK,
    TechpowerupPart.GPU: GPU_UNIQUE_LINK,
    TechpowerupPart.SSD: SSD_UNIQUE_LINK
}

TechpowerupPart.PART_PAGES_COUNT_MAPPING = {
    TechpowerupPart.CPU: CPU_PAGES_COUNT,
    TechpowerupPart.GPU: GPU_PAGES_COUNT,
    TechpowerupPart.SSD: SSD_PAGES_COUNT
}

TechpowerupPart.PART_CLASS_MAPPING = {
    TechpowerupPart.CPU: 'cpuname',
    TechpowerupPart.GPU: 'gpudb-name',
    TechpowerupPart.SSD: 'drivename'
}