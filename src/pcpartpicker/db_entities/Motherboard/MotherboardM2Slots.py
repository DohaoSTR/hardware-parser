from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship 

from ...BaseSQLAlchemy import Base

class MotherboardM2Slots(Base):
    __tablename__ = 'motherboard_m2_slots'

    id = Column(Integer, primary_key=True, autoincrement=True)
    standard_size = Column(Integer)
    key_name = Column(String(10))
    description = Column(String(250))

    motherboard_id = Column(Integer, ForeignKey('motherboard_main_data.id'), nullable=False)
    motherboard = relationship('MotherboardMainData')