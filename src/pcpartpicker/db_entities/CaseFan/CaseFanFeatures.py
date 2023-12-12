from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CaseFanFeatures(Base):
    __tablename__ = 'case_fan_features'

    id = Column(Integer, primary_key=True)
    value = Column(Text, nullable=False)

    part_id = Column(Integer, ForeignKey('part.id'), nullable=False)
    part = relationship("PartEntity")