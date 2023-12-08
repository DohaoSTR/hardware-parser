from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship 

from ...BaseSQLAlchemy import Base

class PowerSupplyData(Base):
    __tablename__ = 'pcpartpicker_power_supply'

    id = Column(Integer, primary_key=True)
    model = Column(String(250))
    type = Column(String(250)) 
    efficiency_rating = Column(String(250))
    wattage = Column(DOUBLE)
    length = Column(DOUBLE)
    modular = Column(String(10))
    color = Column(String(250))
    fan = Column(String(10))

    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'), unique=True)
    part = relationship('PcPartPickerPartEntity')