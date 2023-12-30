from sqlalchemy import DECIMAL, Double, Column, DateTime, Integer, ForeignKey, String, func
from sqlalchemy.orm import relationship

from .BaseSQLAlchemy import Base

class Price(Base):
    __tablename__ = 'dns_price'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    price = Column(DECIMAL(10), nullable=False)
    date_time = Column(DateTime, nullable=False, default=func.now())
    product_id = Column(String(250), ForeignKey('dns_product.uid'), nullable=False)

    product = relationship('Product')