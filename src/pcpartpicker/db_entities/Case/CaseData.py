from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class CaseData(Base):
    __tablename__ = 'case_data'

    id = Column(Integer, primary_key=True)
    power_supply = Column(DOUBLE)
    maximum_video_card_length_with = Column(DOUBLE)
    maximum_video_card_length_without = Column(DOUBLE)
    type = Column(String(250))
    color = Column(String(250))
    side_panel = Column(String(250))
    has_power_supply = Column(String(10))
    power_supply_shroud = Column(String(10))
    length = Column(DOUBLE)
    width = Column(DOUBLE)
    height = Column(DOUBLE)
    model = Column(String(250))
    volume = Column(DOUBLE)

    part_id = Column(Integer, ForeignKey('part.id'), unique=True, nullable=False)
    part = relationship("PartEntity")