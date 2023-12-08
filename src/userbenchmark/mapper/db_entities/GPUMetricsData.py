from sqlalchemy import Column, Integer, ForeignKey 
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class GPUMetricsData(Base):
    __tablename__ = 'gpu_metrics_data'

    id = Column(Integer, primary_key=True)
    effective_3d_gaming_speed = Column(DOUBLE)
    avg_locally_deformable_prt = Column(DOUBLE)
    avg_high_dynamic_range_lighting = Column(DOUBLE)
    avg_render_target_array_gshader = Column(DOUBLE)
    avg_nbody_particle_system = Column(DOUBLE)
    locally_deformable_prt = Column(DOUBLE)
    high_dynamic_range_lighting = Column(DOUBLE)
    render_target_array_gshader = Column(DOUBLE)
    nbody_particle_system = Column(DOUBLE)
    parallax_occlusion_mapping = Column(DOUBLE)
    force_splatted_flocking = Column(DOUBLE)
    avg_parallax_occlusion_mapping = Column(DOUBLE)
    avg_force_splatted_flocking = Column(DOUBLE)

    part_id = Column(Integer, ForeignKey('parts.id'), unique=True, nullable=False)
    part = relationship("PartEntity")