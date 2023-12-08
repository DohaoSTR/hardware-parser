from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CPUCoolerSocket(Base):
    __tablename__ = 'pcpartpicker_cpu_cooler_socket'

    id = Column(Integer, primary_key=True)
    socket = Column(String(250))
    cpu_cooler_id = Column(Integer, ForeignKey('pcpartpicker_cpu_cooler.id'), nullable=False)
    cooler = relationship("CPUCoolerData")