from sqlalchemy import Table, Column, ForeignKey, Integer, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import column, false
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import INTEGER

engine = create_engine("sqlite:///:memory:", future=True)
conn = engine.connect()

Base = declarative_base()

# #  ONE TO MANY
# class Parent(Base):
#     __tablename__ = "parent"
#     id = Column(Integer, primary_key=True)
#     children = relationship("Child")


# class Child(Base):
#     __tablename__ = "child"
#     id = Column(Integer, primary_key=True)
#     parent_id = Column(Integer, ForeignKey("parent.id"))


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
class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    # uselist = false ensures the on-to-one relationship
    child = relationship("Child", back_populates="parent", uselist=False)


class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))

    parent = relationship("Parent", back_populates="child", uselist=False)


# MANY TO MANY - UNIDIRECTIONAL REFERENCE
association_table = Table(
    "association",
    Base.metadata,
    Column("parent_id", ForeignKey("parent.id")),
    Column("child_id", ForeignKey("child.id")),
)


class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    # here the relationship to the Child mapper class is defined through the association table assigned to Relationship.secondary parameter
    children = relationship("Child", secondary=association_table)


class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)


# MANY TO MANY - BIDIRECTIONAL REFERENCE
class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    children = relationship(
        "Child", secondary=association_table, back_populates="parents"
    )


class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    # for a many to many bidirectional reference, back_populates parameter should be passed
    parents = relationship(
        "Parent", secondary=association_table, back_populates="children"
    )


conn.close()
