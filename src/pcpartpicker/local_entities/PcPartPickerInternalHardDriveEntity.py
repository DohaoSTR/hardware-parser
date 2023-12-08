from dataclasses import dataclass

from ..BaseEntity import BaseEntity

from enum import Enum

from ..db_entities.InternalDrive.HDD import HDD
from ..db_entities.InternalDrive.SSD import SSD
from ..db_entities.InternalDrive.HybridStorage import HybridStorage

class InternalDriveType(Enum):
    HDD = "HDD"
    SSD = "SSD"
    HYBRID = "Hybrid"

@dataclass
class PcPartPickerInternalHardDriveEntity(BaseEntity):
    capacity: float = None
    price: float = None
    type: str = None
    cache: float = None
    form_factor: str = None
    interface: str = None
    nvme: str = None
    ssd_nand_flash_type: str = None
    ssd_controller: str = None
    hybrid_ssd_cache: str = None
    model: str = None
    power_loss_protection: str = None

    capacity_measure: str = None
    price_measure: str = None
    cache_measure: str = None
    hybrid_ssd_cache_measure: str = None

    spindle_speed: float = None

    database_type: InternalDriveType = None

    hdd: HDD = None
    ssd: SSD = None
    hybrid_storage: HybridStorage = None

    def __post_init__(self):
        self.capacity, self.capacity_measure = self.handle_parameter_with_measure(self.capacity, float)
        self.price_measure, self.price = self.handle_price_gb(self.price)

        self.hybrid_ssd_cache, self.hybrid_ssd_cache_measure = self.handle_parameter_with_measure(self.hybrid_ssd_cache, float)

        self.cache, self.cache_measure = self.handle_parameter_with_measure(self.cache, float)

        self.ssd_nand_flash_type = self.handle_string_on_na(self.ssd_nand_flash_type)
        self.ssd_controller = self.handle_string_on_na(self.ssd_controller)

        self.database_type, self.spindle_speed = self.handle_type(self.type)

        self.cast_float_fields()
        self.cast_int_fields()

        if self.database_type == InternalDriveType.HDD:
            self.hdd = self.populate_entity("HDD", "part_id")
        
        if self.database_type == InternalDriveType.SSD:
            self.ssd = self.populate_entity("SSD", "part_id")

        if self.database_type == InternalDriveType.HYBRID:
            self.hybrid_storage = self.populate_entity("HybridStorage", "part_id")

    def handle_type(self, type: str):
        if type == 'SSD': 
            return InternalDriveType.SSD, None
        elif type == 'Hybrid':
            return InternalDriveType.HYBRID, None
        else:
            return InternalDriveType.HDD, float(type.replace("RPM", "").replace(" ", ""))