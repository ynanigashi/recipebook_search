from sqlalchemy import Column, Integer, Float,String, text, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

"""
Tables
"""
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hash = Column(String, nullable=False)

    def __repr__(self):
        return f'id: {self.id}, user name: {self.username}, cash: {self.cash}'