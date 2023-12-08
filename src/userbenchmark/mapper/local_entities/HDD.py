from dataclasses import dataclass

from ..BaseEntity import BaseEntity

from ..db_entities.HDDMetricsData import HDDMetricsData
from ..db_entities.PartUserData import PartUserData

@dataclass
class HDD(BaseEntity):
    effective_speed: float = None
    avg_sequential_read_speed: float = None
    avg_sequential_write_speed: float = None
    avg_4k_random_read_speed: float = None
    avg_4k_random_write_speed: float = None
    avg_sequential_mixed_io_speed: float = None
    avg_4k_random_mixed_io_speed: float = None
    avg_sustained_write_speed: float = None
    peak_sequential_read_speed: float = None
    peak_sequential_write_speed: float = None
    peak_4k_random_read_speed: float = None
    peak_4k_random_write_speed: float = None
    peak_sequential_mixed_io_speed: float = None
    peak_4k_random_mixed_io_speed: float = None
    peak_sequential_sustained_write_60s_average: float = None

    capacity: str = None

    ubm_user_rating: str = None
    market_share: str = None
    price: str = None
    vfm: str = None
    newest: str = None

    metrics: HDDMetricsData = None
    user_data: PartUserData = None

    def __post_init__(self):
        self.metrics = self.populate_entity("HDDMetricsData", "part_id")
        self.user_data = self.populate_entity("PartUserData", "part_id")