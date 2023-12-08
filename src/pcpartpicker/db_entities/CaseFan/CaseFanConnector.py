from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CaseFanConnector(Base):
    __tablename__ = 'pcpartpicker_case_fan_connector'

    id = Column(Integer, primary_key=True)
    pin_count = Column(Integer)
    volt_count = Column(Integer)
    rgb = Column(String(10))
    proprietary = Column(String(10))
    addressable = Column(String(10))
    pwm = Column(String(10))
    
    case_fan_id = Column(Integer, ForeignKey('pcpartpicker_case_fan.id'), nullable=False)
    case_fan = relationship("CaseFanData")