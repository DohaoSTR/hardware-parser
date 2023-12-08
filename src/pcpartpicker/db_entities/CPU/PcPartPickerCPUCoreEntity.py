from sqlalchemy import Column, Integer, String, ForeignKey, Double
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class PcPartPickerCPUCoreEntity(Base):
    __tablename__ = 'pcpartpicker_cpu_core'
    
    id = Column(Integer, primary_key=True)

    core_count = Column(Integer)
    performance_core_clock = Column(Double)
    performance_boost_clock = Column(Double)
    microarchitecture = Column(String)
    core_family = Column(String)
    socket = Column(String)
    lithography = Column(Integer)
    integrated_graphics = Column(String)
    simultaneous_multithreading = Column(String)

    cpu_id = Column(Integer, ForeignKey('pcpartpicker_cpu_main_data.id'))
    
    cpu = relationship("PcPartPickerCPUMainDataEntity")