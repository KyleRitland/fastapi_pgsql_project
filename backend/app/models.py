from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

'''

start project code

'''

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, index=True)

    #tweets = relationship("Tweet", back_populates="author")

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    #text = Column(String, index=True)
    text_clean = Column(String, index=True)
    created_at = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.author_id"))

    #author = relationship("Author", back_populates="tweets")