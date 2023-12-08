from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class HDD(Base):
    __tablename__ = 'pcpartpicker_hdd'

    id = Column(Integer, primary_key=True)
    capacity = Column(Float)
    capacity_measure = Column(String(10))
    price = Column(Float)
    price_measure = Column(String(10))
    cache = Column(Float)
    cache_measure = Column(String(10))
    form_factor = Column(String(250))
    interface = Column(String(250))
    model = Column(String(250))
    power_loss_protection = Column(String(10))
    spindle_speed = Column(Float)
    
    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'), nullable=False, unique=True)
    part = relationship("PcPartPickerPartEntity")