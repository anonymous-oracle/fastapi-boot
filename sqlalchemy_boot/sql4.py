from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, declarative_base, relationship
from sqlalchemy.sql.schema import Table

engine = create_engine("sqlite:///:memory:", future=True, echo=True)
Base = declarative_base()


# CREATING A TABLE AND ADDING IT TO THE SAME METADATA COLLECTION
user_table = Table(
    "user_account",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30), nullable=False),
    Column("fullname", String),
)

# CREATING ANOTHER TABLE WITH FOREIGNKEY

address_table = Table(
    "address",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

# INSTEAD OF DECLARING THE MAPPED CLASSES AND THE COLUMN FIELDS WITHIN THE CLASS, WE CAN DECLARE TABLES SEPARATELY AND THEN USE THE SAME
class User(Base):
    __table__ = user_table

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User({self.name!r}, {self.fullname!r})"


class Address(Base):
    __table__ = address_table

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address({self.email_address!r})"


Base.metadata.create_all(engine)
