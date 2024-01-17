from sqlalchemy import Column, Integer

from ..BaseSQLAlchemy import Base

class Metric(Base):
    __tablename__ = 'metric'
    
    id = Column(Integer, primary_key=True)
    gaming_percentage = Column(Integer)
    desktop_percentage = Column(Integer)
    workstation_percentage = Column(Integer)

    part_id = Column(Integer)