from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class HybridStorage(Base):
    __tablename__ = 'hybrid_storage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    capacity = Column(Float)
    capacity_measure = Column(String(10))
    price = Column(Float)
    price_measure = Column(String(10))
    cache = Column(Float)
    cache_measure = Column(String(10))
    hybrid_ssd_cache = Column(Float)
    hybrid_ssd_cache_measure = Column(String(10))
    form_factor = Column(String(250))
    interface = Column(String(250))
    model = Column(String(250))
    power_loss_protection = Column(String(10))

    part_id = Column(Integer, ForeignKey('part.id'), nullable=False, unique=True)
    part = relationship("PartEntity")