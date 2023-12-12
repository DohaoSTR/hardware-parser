from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship 

from ...BaseSQLAlchemy import Base

class PowerSupplyOutput(Base):
    __tablename__ = 'power_supply_output'

    id = Column(Integer, primary_key=True)
    voltage_mode = Column(String(250))
    ampere = Column(DOUBLE)
    power = Column(DOUBLE)
    combined = Column(String(10))
    dc_mode = Column(String(10))
    description = Column(String(250))

    part_id = Column(Integer, ForeignKey('part.id'), unique=False, nullable=False)
    part = relationship("PartEntity")