from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship 

from ...BaseSQLAlchemy import Base

class PowerSupplyEfficiency(Base):
    __tablename__ = 'pcpartpicker_power_supply_efficiency'

    id = Column(Integer, primary_key=True)
    value = Column(String(250), nullable=False)

    power_supply_id = Column(Integer, ForeignKey('pcpartpicker_power_supply.id'), nullable=False)
    power_supply = relationship("PowerSupplyData")