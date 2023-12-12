from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CaseExpansionSlot(Base):
    __tablename__ = 'case_expansion_slot'
    
    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    type = Column(String(250)) 
    riser = Column(String(10))

    part_id = Column(Integer, ForeignKey('part.id'), nullable=False)
    part = relationship("PartEntity")