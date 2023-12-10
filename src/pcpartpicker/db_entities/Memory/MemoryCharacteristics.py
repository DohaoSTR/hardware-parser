from sqlalchemy import Column, Integer, ForeignKey, String, Float, Double
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class MemoryCharacteristics(Base):
    __tablename__ = 'memory_characteristics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    memory_speed = Column(Integer, nullable=True)
    memory_type = Column(String(250), nullable=True)
    pin_count = Column(Integer, nullable=True)
    memory_form_factor = Column(String(250), nullable=True)
    modules_count = Column(Integer, nullable=True)
    modules_memory = Column(Integer, nullable=True)
    modules_memory_measure = Column(String(250), nullable=True)
    first_word_latency = Column(Float, nullable=True)
    voltage = Column(Double, nullable=True)
    cas = Column(Integer, nullable=True)
    trcd = Column(Integer, nullable=True)
    trp = Column(Integer, nullable=True)
    tras = Column(Integer, nullable=True)

    memory_id = Column(Integer, ForeignKey('memory_main_data.id'), unique=True, nullable=False)
    memory = relationship('MemoryMainData')