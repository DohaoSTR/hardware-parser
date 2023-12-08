from sqlalchemy import Column, Integer, String

from ..BaseSQLAlchemy import Base

class PcPartPickerPartEntity(Base):
    __tablename__ = 'pcpartpicker_part'
    
    id = Column(Integer, primary_key=True)
    manufacturer = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    link = Column(String(250), nullable=False) 
    part_type = Column(String(50), nullable=False)
    key = Column(String(50), nullable=False, unique=True)