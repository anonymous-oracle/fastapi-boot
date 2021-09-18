from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import registry, declarative_base, relationship, Session
from sqlalchemy.sql.schema import Table

engine = create_engine("sqlite:///:memory:", future=True, echo=True)
session = Session(engine)
Base = declarative_base()


# INSTEAD OF DECLARING THE MAPPED CLASSES AND THE COLUMN FIELDS WITHIN THE CLASS, WE CAN DECLARE TABLES SEPARATELY AND THEN USE THE SAME
class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    # THE NAMING IN RELATIONSHIP CAN BE UNDERSTOOD BY OBSERVING THE OTHER RELATIONSHIP IN THE MAPPED CLASS TO WHICH IT RELATES TO
    user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id}, email_address={self.email_address})"


Base.metadata.create_all(engine)


# INSERTING THE DATA
stmt = insert(User).values(name="Eren", fullname="Eren Kruger")

compiled = stmt.compile()

print(compiled.params)

# ANOTHER WAY WE CAN INSERT DATA
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

print(result.inserted_primary_key)

with engine.connect() as conn:
    result = conn.execute(
        insert(User),
        [
            {"name": "Grisha", "fullname": "Grisha Jaeger"},
            {"name": "Eren", "fullname": "Eren Jaeger"},
        ],
    )
    conn.commit()


# RETURNING INSERTED VALUES
insert_stmt = (
    insert(Address)
    # .values(name="Levi", fullname="Levi Ackerman")
    .returning(Address.id, Address.email_address)
)
print(insert_stmt)
