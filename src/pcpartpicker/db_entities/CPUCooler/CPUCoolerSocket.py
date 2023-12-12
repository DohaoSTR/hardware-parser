from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CPUCoolerSocket(Base):
    __tablename__ = 'cpu_cooler_socket'

    id = Column(Integer, primary_key=True)
    socket = Column(String(250))
    
    part_id = Column(Integer, ForeignKey('part.id'), nullable=False)
    part = relationship("PartEntity")