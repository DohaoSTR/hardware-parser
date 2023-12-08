from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CaseFanFeatures(Base):
    __tablename__ = 'pcpartpicker_case_fan_features'

    id = Column(Integer, primary_key=True)
    value = Column(Text, nullable=False)

    case_fan_id = Column(Integer, ForeignKey('pcpartpicker_case_fan.id'), nullable=False)
    case_fan = relationship("CaseFanData")