from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class UserRatingEntity(Base):
    __tablename__ = 'user_rating'
    
    id = Column(Integer, primary_key=True)
    ratings_count = Column(Integer)
    average_rating = Column(Float)

    five_star = Column(Integer)
    four_star = Column(Integer)
    three_star = Column(Integer)
    two_star = Column(Integer)
    one_star = Column(Integer)

    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship("PartEntity")