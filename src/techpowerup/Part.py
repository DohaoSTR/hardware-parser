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
class Part(Enum):
    CPU = 'cpu'
    GPU = 'gpu'
    SSD = 'ssd'

    def get_part_enum(part_name: str):
        for part in Part:
            if part_name == part.value:
                return part
            
        return None
    
    def get_part_link(self):
        for part in Part:
            if self == part:
                return part
            
        return None


Part.PART_LINK_MAPPING = {
    Part.CPU: CPU_UNIQUE_LINK,
    Part.GPU: GPU_UNIQUE_LINK,
    Part.SSD: SSD_UNIQUE_LINK
}

Part.PART_PAGES_COUNT_MAPPING = {
    Part.CPU: CPU_PAGES_COUNT,
    Part.GPU: GPU_PAGES_COUNT,
    Part.SSD: SSD_PAGES_COUNT
}

Part.PART_CLASS_MAPPING = {
    Part.CPU: 'cpuname',
    Part.GPU: 'gpudb-name',
    Part.SSD: 'drivename'
}