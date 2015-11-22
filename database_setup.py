import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False)
    relationship("Item", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String(60), nullable=False)
    description = Column(String(500))

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category')


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
