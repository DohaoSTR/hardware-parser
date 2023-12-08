from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class PcPartPickerPartNumber(Base):
    __tablename__ = 'pcpartpicker_part_number'
    
    id = Column(Integer, primary_key=True) 
    part_number = Column(String)
    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'))
    
    part = relationship("PcPartPickerPartEntity")