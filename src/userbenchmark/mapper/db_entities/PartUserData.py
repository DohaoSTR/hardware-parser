from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class PartUserData(Base):
    __tablename__ = 'part_user_data'

    id = Column(Integer, primary_key=True)
    ubm_user_rating = Column(Integer)
    market_share = Column(DOUBLE)
    price = Column(DOUBLE)
    vfm = Column(DOUBLE)
    newest = Column(Integer)

    part_id = Column(Integer, ForeignKey('parts.id'), unique=True, nullable=False)
    part = relationship("PartEntity")