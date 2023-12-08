from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class PcPartPickerUserRatingEntity(Base):
    __tablename__ = 'pcpartpicker_user_rating'
    
    id = Column(Integer, primary_key=True)
    ratings_count = Column(Integer)
    average_rating = Column(Float)

    five_star = Column(Integer)
    four_star = Column(Integer)
    three_star = Column(Integer)
    two_star = Column(Integer)
    one_star = Column(Integer)

    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'))
    
    part = relationship("PcPartPickerPartEntity")