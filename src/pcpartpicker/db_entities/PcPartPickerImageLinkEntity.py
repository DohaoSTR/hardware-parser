from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class PcPartPickerImageLinkEntity(Base):
    __tablename__ = 'pcpartpicker_image_link'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)

    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'))
    
    part = relationship("PcPartPickerPartEntity")