from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class RAMMetricsData(Base):
    __tablename__ = 'ram_metrics_data'

    id = Column(Integer, primary_key=True)
    effective_speed = Column(DOUBLE)
    avg_16_core_read_bench = Column(DOUBLE)
    avg_16_core_write_bench = Column(DOUBLE)
    avg_16_core_mixed_io_bench = Column(DOUBLE)
    sixteen_core_read_bench = Column(DOUBLE)
    sixteen_core_write_bench = Column(DOUBLE)
    sixteen_core_mixed_io_bench = Column(DOUBLE)
    avg_1_core_read_bench = Column(DOUBLE)
    avg_1_core_write_bench = Column(DOUBLE)
    avg_1_core_mixed_io_bench = Column(DOUBLE)
    single_core_read_bench = Column(DOUBLE)
    single_core_write_bench = Column(DOUBLE)
    single_core_mixed_io_bench = Column(DOUBLE)

    part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    part = relationship("PartEntity")