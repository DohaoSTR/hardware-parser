from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CitilinkCompatible(Base):
    __tablename__ = 'citilink_compatible'

    id = Column(Integer, primary_key=True)
    
    citilink_id = Column(Integer, nullable=False)
    pcpartpicker_id = Column(Integer, nullable=False)