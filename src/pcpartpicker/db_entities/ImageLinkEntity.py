from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class ImageLinkEntity(Base):
    __tablename__ = 'image_link'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)

    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship("PartEntity")