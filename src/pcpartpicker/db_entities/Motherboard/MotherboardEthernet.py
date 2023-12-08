from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship 

from ...BaseSQLAlchemy import Base

class MotherboardEthernet(Base):
    __tablename__ = 'pcpartpicker_motherboard_ethernet'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    network_adapter_count = Column(Integer)
    network_adapter_speed = Column(Integer) 
    speed_measure = Column(Integer) 
    network_adapter = Column(String(250))

    motherboard_id = Column(Integer, ForeignKey('pcpartpicker_motherboard_main_data.id'), nullable=False)
    motherboard = relationship('MotherboardMainData')