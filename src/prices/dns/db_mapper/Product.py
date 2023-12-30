from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship

from .BaseSQLAlchemy import Base

class Product(Base):
    __tablename__ = 'dns_product'

    uid = Column(String(250), primary_key=True, nullable=False)
    name = Column(String(250), nullable=False)
    part_number = Column(String(250))
    link = Column(String(250), nullable=False)
    category = Column(String(50), nullable=False)