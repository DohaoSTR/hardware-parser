from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class UserBenchmarkCompatible(Base):
    __tablename__ = 'userbenchmark_compatible'

    id = Column(Integer, primary_key=True)
    
    userbenchmark_id = Column(Integer, nullable=False)
    pcpartpicker_id = Column(Integer, nullable=False)