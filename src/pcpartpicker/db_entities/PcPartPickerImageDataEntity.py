from sqlalchemy import Column, Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class PcPartPickerImageDataEntity(Base):
    __tablename__ = 'pcpartpicker_image_data'
    
    id = Column(Integer, primary_key=True)
    image_data = Column(LargeBinary)
    image_link_data_id = Column(Integer, ForeignKey('pcpartpicker_image_link.id'))
    
    image_link = relationship("PcPartPickerImageLinkEntity")