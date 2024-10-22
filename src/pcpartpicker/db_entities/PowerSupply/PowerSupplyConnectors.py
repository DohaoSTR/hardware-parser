from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship 

from ...BaseSQLAlchemy import Base

class PowerSupplyConnectors(Base):
    __tablename__ = 'power_supply_connectors'

    id = Column(Integer, primary_key=True)
    atx_4pin_connectors = Column(Integer)
    eps_8pin_connectors = Column(Integer)
    pcie_12_4pin_12vhpwr_connectors = Column(Integer)
    pcie_12pin_connectors = Column(Integer)
    pcie_8pin_connectors = Column(Integer)
    pcie_6_2pin_connectors = Column(Integer)
    pcie_6pin_connectors = Column(Integer)
    sata_connectors = Column(Integer)
    molex_4pin_connectors = Column(Integer)

    part_id = Column(Integer, ForeignKey('part.id'), unique=True, nullable=False)
    part = relationship("PartEntity")