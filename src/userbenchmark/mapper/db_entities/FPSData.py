from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from .Games import Games
from ..BaseSQLAlchemy import Base

class FPSData(Base):
    __tablename__ = 'fps_data'

    id = Column(Integer, primary_key=True)
    fps = Column(DOUBLE)
    samples = Column(Integer)
    resolution = Column(Enum('720p', '1080p', '1440p', '4K', 'None'), nullable=False)
    game_settings = Column(Enum('Low', 'Med', 'High', 'Max', 'None'), nullable=False)

    cpu_id = Column(Integer, ForeignKey('parts.id'))
    gpu_id = Column(Integer, ForeignKey('parts.id'))
    game_key = Column(Integer, ForeignKey('games.key'))

    cpu = relationship("PartEntity", foreign_keys=[cpu_id])
    gpu = relationship("PartEntity", foreign_keys=[gpu_id])
    game = relationship("Games", foreign_keys=[game_key])