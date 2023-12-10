from .UserBenchmarkPart import UserBenchmarkPart

from enum import Enum

class UserBenchmarkFPSCombination(Enum):
    CPU = "cpu"
    GPU = "gpu"
    GPU_CPU = "gpu_cpu"

    def get_part_enum(part_name: str):
        for part in UserBenchmarkFPSCombination:
            if part_name == part.value:
                return part
            
        return None

UserBenchmarkFPSCombination.PART_MAPPING = {
    UserBenchmarkFPSCombination.CPU: UserBenchmarkPart.CPU,
    UserBenchmarkFPSCombination.GPU: UserBenchmarkPart.GPU
}

UserBenchmarkFPSCombination.KEY_MAPPING = {
    UserBenchmarkFPSCombination.CPU: "cpu_key",
    UserBenchmarkFPSCombination.GPU: "gpu_key"
}