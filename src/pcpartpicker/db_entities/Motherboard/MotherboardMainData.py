from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class MotherboardMainData(Base):
    __tablename__ = 'pcpartpicker_motherboard_main_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True) 
    
    form_factor = Column(String(250))
    chipset = Column(String(250))
    memory_max = Column(Integer)
    memory_type = Column(String(250))
    memory_slots = Column(Integer)
    color = Column(String(250))
    supports_ecc = Column(String(250))
    raid_support = Column(String(250))
    model = Column(String(250))
    onboard_video = Column(String(250))
    wifi_standard = Column(String(250))
    network_adapter_speed = Column(DOUBLE)

    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'),  unique=True, nullable=False)
    part = relationship('PcPartPickerPartEntity')