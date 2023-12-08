from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class MotherboardMultiInterface(Base):
    __tablename__ = 'pcpartpicker_motherboard_multi_interface'
   
    id = Column(Integer, primary_key=True, autoincrement=True)
    ways_count = Column(Integer) 
    name_technology = Column(String(250))

    motherboard_id = Column(Integer, ForeignKey('pcpartpicker_motherboard_main_data.id'), nullable=False)
    motherboard = relationship('MotherboardMainData')