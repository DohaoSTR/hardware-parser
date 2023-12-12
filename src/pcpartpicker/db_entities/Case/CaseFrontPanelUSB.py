from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CaseFrontPanelUSB(Base):
    __tablename__ = 'case_front_panel_usb'
    
    id = Column(Integer, primary_key=True)
    value = Column(String(250), nullable=False)
    
    part_id = Column(Integer, ForeignKey('part.id'), nullable=False)
    part = relationship("PartEntity")