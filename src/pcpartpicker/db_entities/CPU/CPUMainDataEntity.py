from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CPUMainDataEntity(Base):
    __tablename__ = 'cpu_main_data'
    
    id = Column(Integer, primary_key=True)

    tdp = Column(Integer)
    series = Column(String)
    maximum_supported_memory = Column(Integer)
    ecc_support = Column(String)
    includes_cooler = Column(String)
    packaging = Column(String)
    model = Column(String)

    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship("PartEntity")