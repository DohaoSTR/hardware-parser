from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CPUCoolerData(Base):
    __tablename__ = 'pcpartpicker_cpu_cooler'

    id = Column(Integer, primary_key=True)
    model = Column(String(250))
    height = Column(DOUBLE)
    water_cooled = Column(DOUBLE)
    fan = Column(String(10))
    color = Column(String(250))
    bearing = Column(String(250))
    min_rpm = Column(DOUBLE)
    max_rpm = Column(DOUBLE)
    min_noise_level = Column(DOUBLE)
    max_noise_level = Column(DOUBLE)

    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'), unique=True)
    part = relationship("PcPartPickerPartEntity")