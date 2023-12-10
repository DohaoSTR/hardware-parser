from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class SSDMetricsData(Base):
    __tablename__ = 'ssd_metrics_data'

    id = Column(Integer, primary_key=True)
    effective_speed = Column(DOUBLE)
    avg_sequential_read_speed = Column(DOUBLE)
    avg_sequential_write_speed = Column(DOUBLE)
    avg_4k_random_read_speed = Column(DOUBLE)
    avg_4k_random_write_speed = Column(DOUBLE)
    avg_sequential_mixed_io_speed = Column(DOUBLE)
    avg_4k_random_mixed_io_speed = Column(DOUBLE)
    avg_sustained_write_speed = Column(DOUBLE)
    peak_sequential_read_speed = Column(DOUBLE)
    peak_sequential_write_speed = Column(DOUBLE)
    peak_4k_random_read_speed = Column(DOUBLE)
    peak_4k_random_write_speed = Column(DOUBLE)
    peak_sequential_mixed_io_speed = Column(DOUBLE)
    peak_4k_random_mixed_io_speed = Column(DOUBLE)
    peak_sequential_sustained_write_60s_average = Column(DOUBLE)
    peak_4k_64_thread_read_speed = Column(DOUBLE)
    peak_4k_64_thread_write_speed = Column(DOUBLE)
    peak_4k_64_thread_mixed_io_speed = Column(DOUBLE)
    avg_4k_64_thread_read_speed = Column(DOUBLE)
    avg_4k_64_thread_write_speed = Column(DOUBLE)
    avg_4k_64_thread_mixed_io_speed = Column(DOUBLE)

    part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    part = relationship("PartEntity")