from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import DOUBLE

from ..BaseSQLAlchemy import Base

class PartEntity(Base):
    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True)
    type = Column(String(250))
    part_number = Column(String(250))
    brand = Column(String(250))
    model = Column(String(250))
    rank = Column(Integer)
    benchmark = Column(DOUBLE)
    samples = Column(Integer)
    url = Column(String(250))