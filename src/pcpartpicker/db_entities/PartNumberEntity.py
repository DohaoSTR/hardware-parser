from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class PartNumberEntity(Base):
    __tablename__ = 'part_number'
    
    id = Column(Integer, primary_key=True) 
    part_number = Column(String)
    
    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship("PartEntity")