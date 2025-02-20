"""db models"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, \
    Boolean, BigInteger, SmallInteger, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """parent DB base class"""


class DbLog(Base):
    """лог-файл"""
    __tablename__ = "logs"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    log_string = Column(Text, nullable=False)
    created_at = Column(DateTime(), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}: {self.log_string[:50]}"
