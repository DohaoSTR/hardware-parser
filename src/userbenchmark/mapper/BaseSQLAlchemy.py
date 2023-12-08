from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseEntity:
    def is_empty(self):
        for column in self.__table__.columns:
            if getattr(self, column.name) is not None:
                return False
        return True