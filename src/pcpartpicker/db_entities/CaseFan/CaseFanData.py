from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CaseFanData(Base):
    __tablename__ = 'case_fan'

    id = Column(Integer, primary_key=True)
    model = Column(String(250))
    size = Column(DOUBLE)
    color = Column(String(250))
    quantity = Column(Integer)
    pwm = Column(String(10))
    led = Column(String(250))
    controller = Column(String(250))
    static_pressure = Column(DOUBLE)
    bearing_type = Column(String(250))
    min_rpm = Column(DOUBLE) 
    max_rpm = Column(DOUBLE)
    min_airflow = Column(DOUBLE)
    max_airflow = Column(DOUBLE)
    min_noise_level = Column(DOUBLE)
    max_noise_level = Column(DOUBLE)
    
    part_id = Column(Integer, ForeignKey('part.id'), unique=True)
    part = relationship("PartEntity")