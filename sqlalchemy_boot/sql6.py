from sqlalchemy import Table, Column, ForeignKey, Integer, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import PrimaryKeyConstraint

engine = create_engine("sqlite:///:memory:", future=True)
conn = engine.connect()

Base = declarative_base()

#  ONE TO MANY
class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    children = relationship("Child")


class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))


# BIDIRECTIONAL ONE TO MANY WHERE THE REVERSE IS A MANY TO ONE RELATIONSHIP
class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")


class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))
    parent = relationship("Parent", back_populates="children")


# MANY TO ONE
class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("child.id"))
    child = relationship("Child", back_populates="parents")


class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    parents = relationship("Child", back_populates="child")


# ONE TO ONE

conn.close()
