from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class GPUMainData(Base):
    __tablename__ = 'pcpartpicker_gpu_main_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String(250), default=None)
    chipset = Column(String(250), default=None)
    memory = Column(Float, default=None)
    memory_type = Column(String(250), default=None)
    core_clock = Column(Integer, default=None)
    boost_clock = Column(Integer, default=None)
    effective_memory_clock = Column(Integer, default=None)
    color = Column(String(250), default=None)
    frame_sync = Column(String(250), default=None)
    tdp = Column(Integer, default=None)
    radiator_mm = Column(Integer, default=None)
    fans_count = Column(Integer, default=None)

    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'), unique=True, nullable=False)
    part = relationship("PcPartPickerPartEntity")