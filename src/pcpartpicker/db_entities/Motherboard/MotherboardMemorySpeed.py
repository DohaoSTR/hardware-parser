from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class MotherboardMemorySpeed(Base):
    __tablename__ = 'pcpartpicker_motherboard_memory_speed'

    id = Column(Integer, primary_key=True, autoincrement=True)
    memory_type = Column(String(10))
    memory_speed = Column(Integer) 

    motherboard_id = Column(Integer, ForeignKey('pcpartpicker_motherboard_main_data.id'), nullable=False)
    motherboard = relationship('MotherboardMainData')