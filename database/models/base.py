from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """
    Базовая модель таблицы.

    id: int - id записи.
    """

    __abstract__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
