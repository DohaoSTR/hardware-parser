from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class DNSCompatible(Base):
    __tablename__ = 'dns_compatible'

    id = Column(Integer, primary_key=True)

    dns_uid = Column(String(250), nullable=False)
    pcpartpicker_id = Column(Integer, nullable=False)