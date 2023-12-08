from dataclasses import dataclass

from ..BaseEntity import BaseEntity

from ..db_entities.GPUMetricsData import GPUMetricsData
from ..db_entities.PartUserData import PartUserData

@dataclass
class GPU(BaseEntity):
    effective_3d_gaming_speed: float = None
    avg_locally_deformable_prt: float = None
    avg_high_dynamic_range_lighting: float = None
    avg_render_target_array_gshader: float = None
    avg_nbody_particle_system: float = None
    locally_deformable_prt: float = None
    high_dynamic_range_lighting: float = None
    render_target_array_gshader: float = None
    nbody_particle_system: float = None
    parallax_occlusion_mapping: float = None
    force_splatted_flocking: float = None
    avg_parallax_occlusion_mapping: float = None
    avg_force_splatted_flocking: float = None

    ubm_user_rating: str = None
    market_share: str = None
    price: str = None
    vfm: str = None
    newest: str = None

    metrics: GPUMetricsData = None
    user_data: PartUserData = None

    def __post_init__(self):
        self.metrics = self.populate_entity("GPUMetricsData", "part_id")
        self.user_data = self.populate_entity("PartUserData", "part_id")