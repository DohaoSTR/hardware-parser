from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class CPUMetricsData(Base):
    __tablename__ = 'cpu_metrics_data'

    id = Column(Integer, primary_key=True)
    effective_speed = Column(DOUBLE)
    avg_memory_latency = Column(DOUBLE)
    avg_single_core_speed = Column(DOUBLE)
    avg_dual_core_speed = Column(DOUBLE)
    avg_quad_core_speed = Column(DOUBLE)
    avg_octa_core_speed = Column(DOUBLE)
    avg_multi_core_speed = Column(DOUBLE)
    oc_memory_core_speed = Column(DOUBLE)
    oc_single_core_speed = Column(DOUBLE)
    oc_dual_core_speed = Column(DOUBLE)
    oc_quad_core_speed = Column(DOUBLE)
    oc_octa_core_speed = Column(DOUBLE)
    oc_multi_core_speed = Column(DOUBLE)

    part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    part = relationship("PartEntity")