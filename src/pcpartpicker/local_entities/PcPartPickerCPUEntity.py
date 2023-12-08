from dataclasses import dataclass

from ..db_entities.CPU.PcPartPickerCPUCacheEntity import PcPartPickerCPUCacheEntity
from ..db_entities.CPU.CPUCacheType import CPUCacheType
from ..db_entities.CPU.PcPartPickerCPUCoreEntity import PcPartPickerCPUCoreEntity
from ..db_entities.CPU.PcPartPickerCPUMainDataEntity import PcPartPickerCPUMainDataEntity

from ..BaseEntity import BaseEntity

@dataclass
class PcPartPickerCPUEntity(BaseEntity):
    core_count: int = None
    performance_core_clock: float = None
    performance_boost_clock: float = None
    microarchitecture: str = None
    core_family: str = None
    socket: str = None
    lithography: int = None
    integrated_graphics: str = None
    simultaneous_multithreading: str = None

    tdp: int = None
    series: str = None
    maximum_supported_memory: int = None
    ecc_support: str = None
    includes_cooler: str = None
    packaging: str = None
    model: str = None

    performance_l1_cache: list = None
    performance_l2_cache: str = None
    l3_cache: str = None

    efficiency_l1_cache: list = None
    efficiency_l2_cache: str = None

    main_data: PcPartPickerCPUMainDataEntity = None
    cpu_core: PcPartPickerCPUCoreEntity = None
    perfomance_cache: PcPartPickerCPUCacheEntity = None
    efficiency_cache: PcPartPickerCPUCacheEntity = None

    def __populate_cache_entity(self, cache_type: CPUCacheType):
        cache_vars = self.handle_l1_cache(getattr(self, f"{cache_type.value}_l1_cache"))
        l2_cache_vars = self.handle_l2_l3_cache(getattr(self, f"{cache_type.value}_l2_cache"))

        if cache_type == CPUCacheType.Efficiency:
            l3_cache_vars = (None, None, None)
        else:
            l3_cache_vars = self.handle_l2_l3_cache(getattr(self, f"l3_cache"))

        cache_entity = PcPartPickerCPUCacheEntity(
            count_lines_l1_instruction=cache_vars[0],
            capacity_l1_instruction=cache_vars[1],
            capacity_measure_l1_instruction=cache_vars[2],
            count_lines_l1_data=cache_vars[3],
            capacity_l1_data=cache_vars[4],
            capacity_measure_l1_data=cache_vars[5],

            count_lines_l2=l2_cache_vars[0],
            capacity_l2=l2_cache_vars[1],
            capacity_measure_l2=l2_cache_vars[2],

            count_lines_l3=l3_cache_vars[0],
            capacity_l3=l3_cache_vars[1],
            capacity_measure_l3=l3_cache_vars[2],
        )

        if cache_entity.is_empty() == True:
            cache_entity = None
        else:
            cache_entity.type = cache_type.value

        return cache_entity
    
    def __populate_main_data_entity(cpu_entity) -> PcPartPickerCPUMainDataEntity:
        db_entity = PcPartPickerCPUMainDataEntity()

        for column_name in db_entity.__table__.columns.keys():
            if column_name != "id" and column_name != "part_id":
                setattr(db_entity, column_name, getattr(cpu_entity, column_name))

        return db_entity
    
    def __populate_cpu_core_entity(cpu_entity) -> PcPartPickerCPUCoreEntity:
        db_entity = PcPartPickerCPUCoreEntity()

        for column_name in db_entity.__table__.columns.keys():
            if column_name != "id" and column_name != "cpu_id":
                setattr(db_entity, column_name, getattr(cpu_entity, column_name))

        return db_entity
    
    def __post_init__(self):
        self.performance_core_clock = self.handle_parameter(self.performance_core_clock, float, "GHz")
        self.performance_boost_clock = self.handle_parameter(self.performance_boost_clock, float, "GHz")

        self.lithography = self.handle_parameter(self.lithography, int, "nm")
        
        self.integrated_graphics = self.handle_str_none(self.integrated_graphics)
        
        self.tdp = self.handle_parameter(self.tdp, int, "W")
        self.maximum_supported_memory = self.handle_parameter(self.maximum_supported_memory, int, "GB")

        self.main_data = self.__populate_main_data_entity()
        self.cpu_core = self.__populate_cpu_core_entity()
        
        self.perfomance_cache = self.__populate_cache_entity(CPUCacheType.Performance)
        self.efficiency_cache = self.__populate_cache_entity(CPUCacheType.Efficiency)

        self.cast_int_fields()