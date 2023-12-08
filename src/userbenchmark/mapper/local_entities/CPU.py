from dataclasses import dataclass

from ..BaseEntity import BaseEntity

from ..db_entities.CPUMetricsData import CPUMetricsData
from ..db_entities.PartUserData import PartUserData

@dataclass
class CPU(BaseEntity):
    effective_speed: float = None
    avg_memory_latency: float = None
    avg_single_core_speed: float = None
    avg_dual_core_speed: float = None
    avg_quad_core_speed: float = None
    avg_octa_core_speed: float = None
    avg_multi_core_speed: float = None
    oc_memory_core_speed: float = None
    oc_single_core_speed: float = None
    oc_dual_core_speed: float = None
    oc_quad_core_speed: float = None
    oc_octa_core_speed: float = None
    oc_multi_core_speed: float = None

    ubm_user_rating: str = None
    market_share: str = None
    price: str = None
    vfm: str = None
    newest: str = None

    tdp: str = None
    processing_cores: str = None
    processing_threads: str = None
    manufacturing_process: str = None
    base_clock_speed: str = None
    turbo_clock_speed: str = None
    series_architecture: str = None
    socket: str = None
    integrated_graphics: str = None

    metrics: CPUMetricsData = None
    user_data: PartUserData = None

    def __post_init__(self):
        self.metrics = self.populate_entity("CPUMetricsData", "part_id")
        self.user_data = self.populate_entity("PartUserData", "part_id")