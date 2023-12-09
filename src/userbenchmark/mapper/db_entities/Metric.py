from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class Metric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True)
    gaming_percentage = Column(Integer, nullable=False)
    desktop_percentage = Column(Integer, nullable=False)
    workstation_percentage = Column(Integer, nullable=False)

    part_id = Column(Integer, ForeignKey('parts.id'), unique=True, nullable=False)
    part = relationship("PartEntity")