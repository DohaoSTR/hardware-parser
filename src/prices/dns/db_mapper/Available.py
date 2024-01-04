from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .BaseSQLAlchemy import Base

class Available(Base):
    __tablename__ = 'dns_available'

    id = Column(Integer, primary_key=True)
    status = Column(String(250, collation='utf8mb4_unicode_ci'), nullable=True)
    delivery_info = Column(String(250, collation='utf8mb4_unicode_ci'), nullable=True)
    date_time = Column(DateTime, nullable=False)
    city_name = Column(String(250, collation='utf8mb4_unicode_ci'), nullable=False)

    product_id = Column(String(250, collation='utf8mb4_unicode_ci'), ForeignKey('dns_product.uid'), nullable=False)
    product = relationship('Product')