from operator import and_, or_
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import registry, declarative_base, relationship, Session
from sqlalchemy.sql.elements import literal_column
from sqlalchemy.sql.expression import desc, text
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Table

engine = create_engine("sqlite:///:memory:", future=True, echo=False)
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
print()

# INSERTING THE DATA
stmt = insert(User).values(name="Eren", fullname="Eren Kruger")

compiled = stmt.compile()

print(compiled.params)
print()

# ANOTHER WAY WE CAN INSERT DATA
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

print(result.inserted_primary_key)
print()

with engine.connect() as conn:
    result = conn.execute(
        insert(User),
        [
            {"name": "Grisha", "fullname": "Grisha Jaeger"},
            {"name": "Eren", "fullname": "Eren Jaeger"},
        ],
    )

    conn.execute(
        insert(Address),
        [
            {
                "email_address": "eren@marley.com",
                "user_id": 3,
            },
            {
                "email_address": "eren@paradis.com",
                "user_id": 1,
            },
        ],
    )

    conn.commit()
print()

# RETURNING INSERTED VALUES
insert_stmt = (
    insert(Address)
    # .values(name="Levi", fullname="Levi Ackerman")
    .returning(Address.id, Address.email_address)
)
print(insert_stmt)
print()

# SELECTING ROWS
stmt = select(User).where(User.name == "Eren")
print(stmt)
print()

# USING engine.connect()
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)
print()

# USING Session object
with Session(engine) as sess:
    for row in sess.execute(stmt):
        print(row)
print()

# SELECTING SPECIFIC COLUMNS
print(select(User.name, User.fullname))
print()

# SELECTING ORM ENTITIES AND COLUMNS
print(select(User))
print()
with Session(engine) as sess:
    # this would be the same as 'select * from user_account limit 1'
    row = sess.execute(select(User)).first()
    print(row[0])
print()

# SELECTING USING ORM CLAUSES
stmt = select(User).where(User.name == "Eren").order_by(User.name)
print(stmt)
print()
with Session(engine) as sess:
    print(sess.execute(stmt).all())
print()

# LABELLING QUERY RESULTS
stmt = select(("Username: " + User.name).label("username")).order_by(User.name)
with Session(engine) as sess:
    for row in sess.execute(stmt):
        # the .username refers to the label name given in the .label method
        print(f"{row.username}")
print()

# GENERATING CONSTANT SQL EXPRESSIONS

# Note: make sure that the constant expression is further enclosed within single quotes
stmt = select(text("'CONSTANT_EXPRESSION'"), User.name, User.fullname).order_by(
    User.name
)
with engine.connect() as conn:
    for row in conn.execute(stmt).all():
        print(f"{row}")

# Since we represented a single column, we can use another function instead of text()
stmt = select(
    literal_column("'CONTANT_EXPRESSION'"), User.name, User.fullname
).order_by(User.name)
with engine.connect() as conn:
    for row in conn.execute(stmt).all():
        print(f"{row}")
print()

# WHERE CLAUSE
print(User.id > 2)

print(User.name == "Eren")

print()
print(select(User).where(User.id > 1).where(User.id < 4))

# OR
print()
print(select(User).where(User.id > 1, User.id < 4))
print()

# AND and OR conjunctions
stmt = select(User).where(and_(User.name == "Eren", or_(User.id > 1, User.id < 4)))
print(stmt)
with engine.connect() as conn:
    print(conn.execute(stmt).all())
print()

# FILTER BY CLAUSE
stmt = select(User).filter_by(name="Eren", id=1)
print(stmt)
with Session(engine) as sess:
    for row in sess.execute(stmt).all():
        print(row[0])
print()

# TEST
stmt = select(Address)
print(stmt)
with Session(engine) as sess:
    for row in sess.execute(stmt).all():
        print(row[0].user_id)
print()

# JOIN STATEMENTS: TYPE 1
stmt = select(
    User.name, User.fullname, Address.email_address, User.id, Address.user_id
).join_from(User, Address)
print(stmt)
with Session(engine) as sess:
    for row in sess.execute(stmt).all():
        print(row)
print()

# JOIN STATEMENTS: TYPE 2
stmt = select(
    User.name, User.fullname, Address.email_address, User.id, Address.user_id
).join(Address)
print(stmt)
with Session(engine) as sess:
    for row in sess.execute(stmt).all():
        print(row)
print()

# JOIN STATEMENTS: TYPE 3
stmt = (
    select(User.name, User.fullname, Address.email_address, User.id, Address.user_id)
    .select_from(User)
    .join(Address)
)
print(stmt)
with Session(engine) as sess:
    for row in sess.execute(stmt).all():
        print(row)
print()

# AN AGGREGATOR FUNCTION
stmt = select(func.count("*")).select_from(User)
print(stmt)
with engine.connect() as conn:
    for row in conn.execute(stmt).all():
        print(row)
print()

# JOIN STATEMENTS: TYPE 4 - SETTING THE ON CLAUSE
stmt = (
    select(
        User.name,
        User.fullname,
        Address.email_address,
        Address.id,
        User.id,
        Address.user_id,
    )
    .select_from(User)
    .join(Address, User.id == Address.id)
)
print(stmt)
with Session(engine) as sess:
    for row in sess.execute(stmt).all():
        print(row)
print()

# OUTER JOIN
print(select(User).join(Address, isouter=True))
print()

# FULL JOIN
print(select(User).join(Address, full=True))
print()

# ORDER BY
print(select(User).order_by(User.name))
print(select(User).order_by(User.name.desc()))
print()

# GROUP BY
count_qry = select(func.count(User.id))
print(count_qry)
print()

stmt = (
    select(User.name, func.count(Address.id).label("count"))
    .join(Address)
    .group_by(User.name)
    .having(func.count(Address.id > 1))
)
print(stmt)
with Session(engine) as sess:
    for row in sess.execute(stmt).all():
        print(row)
print()

# ORDER BY WITH GROUP BY
stmt = (
    select(User.name, func.count(Address.id).label("count"))
    .join(Address)
    .group_by(User.name)
    .order_by(Address.user_id, desc("count"))
)
print(stmt)
with Session(engine) as sess:
    for row in sess.execute(stmt).all():
        print(row)
print()
