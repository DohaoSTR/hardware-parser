from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class GPUMultiInterfaceData(Base):
    __tablename__ = 'pcpartpicker_gpu_multi_interface_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ways_count = Column(Integer, default=None)
    name_technology = Column(String(250), default=None)

    gpu_id = Column(Integer, ForeignKey('pcpartpicker_gpu_main_data.id'), unique=False, nullable=False)
    gpu = relationship("GPUMainData")
