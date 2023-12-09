from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class PartsCompareKey(Base):
    __tablename__ = 'parts_compare_keys'

    id = Column(Integer, primary_key=True)
    key = Column(Integer, nullable=False)
    type = Column(String(10), nullable=False)

    part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    part = relationship("PartEntity")