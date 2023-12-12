from sqlalchemy import Column, Integer, String, ForeignKey, Double
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CPUCoreEntity(Base):
    __tablename__ = 'cpu_core'
    
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

    part_id = Column(Integer, ForeignKey('part.id'), nullable=False)
    part = relationship("PartEntity")