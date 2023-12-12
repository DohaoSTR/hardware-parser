from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship 

from ...BaseSQLAlchemy import Base

class MotherboardConnectData(Base):
    __tablename__ = 'motherboard_connect_data'
    
    id = Column(Integer, primary_key=True)
    
    pcie_x16_slots = Column(Integer)
    pcie_x8_slots = Column(Integer) 
    pcie_x4_slots = Column(Integer)
    pcie_x1_slots = Column(Integer)
    pci_slots = Column(Integer)
    mini_pcie_slots = Column(Integer)
    half_mini_pcie_slots = Column(Integer)
    mini_pcie_msata_slots = Column(Integer)
    msata_slots = Column(Integer)
    sata_6_0 = Column(Integer)
    pata_100 = Column(Integer)
    sata_3_0 = Column(Integer)
    esata_6_0 = Column(Integer)
    u_2 = Column(Integer)
    esata_3_0 = Column(Integer)
    sas_3_0 = Column(Integer)
    pata_133 = Column(Integer)
    sas_12_0 = Column(Integer)
    sas_6_0 = Column(Integer)
    sata_1_5 = Column(Integer)

    part_id = Column(Integer, ForeignKey('part.id'), unique=True, nullable=False)
    part = relationship("PartEntity")