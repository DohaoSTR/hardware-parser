from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class PartsKey(Base):
    __tablename__ = 'parts_keys'

    id = Column(Integer, primary_key=True)
    key = Column(Integer, nullable=False)
    
    part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    part = relationship("PartEntity")