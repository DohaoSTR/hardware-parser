from datetime import datetime

from sqlalchemy import Boolean, String, create_engine, Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

from .BaseSQLAlchemy import Base

class Available(Base):
    __tablename__ = 'citilink_available'

    id = Column(Integer, primary_key=True)
    is_available = Column(Boolean, nullable=False)
    city_name = Column(String(250), nullable=False)
    product_id = Column(Integer, ForeignKey('citilink_product.id'), nullable=False)
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    product = relationship('Product')