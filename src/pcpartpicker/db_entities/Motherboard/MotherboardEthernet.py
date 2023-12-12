from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship 

from ...BaseSQLAlchemy import Base

class MotherboardEthernet(Base):
    __tablename__ = 'motherboard_ethernet'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    network_adapter_count = Column(Integer)
    network_adapter_speed = Column(Integer) 
    speed_measure = Column(Integer) 
    network_adapter = Column(String(250))

    part_id = Column(Integer, ForeignKey('part.id'), unique=False, nullable=False)
    part = relationship("PartEntity")