from sqlalchemy import Column, Integer, LargeBinary, String

from ..BaseSQLAlchemy import Base

class Games(Base):
    __tablename__ = 'games'
    
    key = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)