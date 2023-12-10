from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class MotherboardSocket(Base):
    __tablename__ = 'motherboard_socket'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    socket_count = Column(Integer)
    socket_name = Column(String(250))

    motherboard_id = Column(Integer, ForeignKey('motherboard_main_data.id'), nullable=False)
    motherboard = relationship('MotherboardMainData')