from dataclasses import dataclass

from ..BaseEntity import BaseEntity

from ..db_entities.RAMMetricsData import RAMMetricsData
from ..db_entities.PartUserData import PartUserData

@dataclass
class RAM(BaseEntity):
    effective_speed: float = None
    avg_16_core_read_bench: float = None
    avg_16_core_write_bench: float = None
    avg_16_core_mixed_io_bench: float = None
    sixteen_core_read_bench: float = None
    sixteen_core_write_bench: float = None
    sixteen_core_mixed_io_bench: float = None
    avg_1_core_read_bench: float = None
    avg_1_core_write_bench: float = None
    avg_1_core_mixed_io_bench: float = None
    single_core_read_bench: float = None
    single_core_write_bench: float = None
    single_core_mixed_io_bench: float = None

    avg_physical_ram_latency: str = None
    physical_ram_latency: str = None
    capacity: str = None

    ubm_user_rating: str = None
    market_share: str = None
    price: str = None
    vfm: str = None
    newest: str = None

    metrics: RAMMetricsData = None
    user_data: PartUserData = None

    def __post_init__(self):
        self.metrics = self.populate_entity("RAMMetricsData", "part_id")
        self.user_data = self.populate_entity("PartUserData", "part_id")