from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CaseDriveBay(Base):
    __tablename__ = 'case_drive_bay'

    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    type = Column(String(250))
    format = Column(DOUBLE)

    part_id = Column(Integer, ForeignKey('part.id'), nullable=False)
    part = relationship("PartEntity")