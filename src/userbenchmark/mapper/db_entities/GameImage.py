from sqlalchemy import Column, Integer, LargeBinary, ForeignKey, String
from sqlalchemy.orm import relationship

from ..BaseSQLAlchemy import Base

class GameImage(Base):
    __tablename__ = 'game_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_data = Column(LargeBinary, nullable=False)
    image_link = Column(String(250), nullable=False)
    game_key = Column(Integer, ForeignKey('games.key'), nullable=False)

    game = relationship('Games')