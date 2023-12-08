from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class PcPartPickerPartPriceEntity(Base):
    __tablename__ = 'pcpartpicker_price_data'

    id = Column(Integer, primary_key=True)
    merchant_link = Column(String)
    merchant_name = Column(String)
    base_price = Column(Float)
    promo_value = Column(Float)
    shipping_text = Column(String)
    shipping_link = Column(String)  
    tax_value = Column(Float)
    availability = Column(String)
    final_price = Column(Float)
    currency = Column(String)
    last_update_time = Column(DateTime)
    part_id = Column(Integer, ForeignKey('pcpartpicker_part.id'))

    part = relationship("PcPartPickerPartEntity")