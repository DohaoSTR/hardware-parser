from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class GPUExternalPowerData(Base):
    __tablename__ = 'gpu_external_power_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    interface_name = Column(String(250), default=None)
    interface_count = Column(Integer, default=None)
    pin_count = Column(Integer, default=None)

    part_id = Column(Integer, ForeignKey('part.id'), unique=False, nullable=False)
    part = relationship("PartEntity")