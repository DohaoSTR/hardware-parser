from sqlalchemy import create_engine, Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

from .BaseSQLAlchemy import Base

class Price(Base):
    __tablename__ = 'citilink_price'

    id = Column(Integer, primary_key=True, nullable=False)
    price = Column(Float(precision=10), nullable=False)
    date_time = Column(DateTime, nullable=False)
    product_id = Column(Integer, ForeignKey('citilink_product.id'), nullable=False)

    product = relationship('Product')