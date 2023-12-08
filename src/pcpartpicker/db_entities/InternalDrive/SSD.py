from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class SSD(Base):
    __tablename__ = 'pcpartpicker_ssd'

    id = Column(Integer, primary_key=True, autoincrement=True)
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
    nvme = Column(String(10))
    ssd_nand_flash_type = Column(String(250))
    ssd_controller = Column(String(250))

    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'), nullable=False, unique=True)
    part = relationship("PcPartPickerPartEntity")