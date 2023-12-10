from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class GPUConnectData(Base):
    __tablename__ = 'gpu_connect_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    interface = Column(String(250), default=None)
    length = Column(Integer, default=None)
    case_expansion_slot_width = Column(Integer, default=None)
    total_slot_width = Column(Integer, default=None)

    gpu_id = Column(Integer, ForeignKey('gpu_main_data.id'), unique=False, nullable=False)
    gpu = relationship("GPUMainData")