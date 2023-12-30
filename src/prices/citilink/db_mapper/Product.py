from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from .BaseSQLAlchemy import Base

class Product(Base):
    __tablename__ = 'citilink_product'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    link = Column(String(250), nullable=False)
    part_number = Column(String(250), nullable=True)
    category= Column(String(250), nullable=False)