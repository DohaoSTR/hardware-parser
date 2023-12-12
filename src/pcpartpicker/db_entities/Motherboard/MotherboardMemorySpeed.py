from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class MotherboardMemorySpeed(Base):
    __tablename__ = 'motherboard_memory_speed'

    id = Column(Integer, primary_key=True, autoincrement=True)
    memory_type = Column(String(10))
    memory_speed = Column(Integer) 

    part_id = Column(Integer, ForeignKey('part.id'), unique=False, nullable=False)
    part = relationship("PartEntity")