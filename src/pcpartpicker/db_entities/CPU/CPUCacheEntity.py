from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base, BaseEntity

class CPUCacheEntity(Base, BaseEntity):
    __tablename__ = 'cpu_cache'
    
    id = Column(Integer, primary_key=True)

    count_lines_l1_instruction = Column(Integer)
    capacity_l1_instruction = Column(Integer)
    capacity_measure_l1_instruction = Column(String)

    count_lines_l1_data = Column(Integer)
    capacity_l1_data = Column(Integer)
    capacity_measure_l1_data = Column(String)

    count_lines_l2 = Column(Integer)
    capacity_l2 = Column(Integer)
    capacity_measure_l2 = Column(String)

    count_lines_l3 = Column(Integer)
    capacity_l3 = Column(Integer)
    capacity_measure_l3 = Column(String)
    
    type = Column(Enum('performance', 'efficiency'))

    part_id = Column(Integer, ForeignKey('part.id'), nullable=False)
    part = relationship("PartEntity")