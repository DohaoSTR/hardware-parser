from .Part import Part

from enum import Enum

class FPSCombination(Enum):
    CPU = "cpu"
    GPU = "gpu"
    GPU_CPU = "gpu_cpu"

    def get_part_enum(part_name: str):
        for part in FPSCombination:
            if part_name == part.value:
                return part
            
        return None

FPSCombination.PART_MAPPING = {
    FPSCombination.CPU: Part.CPU,
    FPSCombination.GPU: Part.GPU
}

FPSCombination.KEY_MAPPING = {
    FPSCombination.CPU: "cpu_key",
    FPSCombination.GPU: "gpu_key"
}