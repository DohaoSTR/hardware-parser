from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class MemoryMainData(Base):
    __tablename__ = 'memory_main_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(10), nullable=True)
    price_gb = Column(Float, nullable=True)
    color = Column(String(250), nullable=True)
    register_memory = Column(String(10), nullable=True)
    ecc = Column(String(10), nullable=True)
    heat_spreader = Column(String(10), nullable=True)
    model = Column(String(250), nullable=True)

    part_id = Column(Integer, ForeignKey('part.id'), unique=True, nullable=False)
    part = relationship('PartEntity')
