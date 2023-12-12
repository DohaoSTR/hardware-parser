from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship 

from ...BaseSQLAlchemy import Base

class PowerSupplyEfficiency(Base):
    __tablename__ = 'power_supply_efficiency'

    id = Column(Integer, primary_key=True)
    value = Column(String(250), nullable=False)

    part_id = Column(Integer, ForeignKey('part.id'), unique=False, nullable=False)
    part = relationship("PartEntity")