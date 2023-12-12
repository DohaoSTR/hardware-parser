from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class MotherboardMultiInterface(Base):
    __tablename__ = 'motherboard_multi_interface'
   
    id = Column(Integer, primary_key=True, autoincrement=True)
    ways_count = Column(Integer) 
    name_technology = Column(String(250))

    part_id = Column(Integer, ForeignKey('part.id'), unique=False, nullable=False)
    part = relationship("PartEntity")