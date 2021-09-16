from sqlalchemy import MetaData, Table, Integer, Column, String, ForeignKey
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True, future=True)

metadata_obj = MetaData()

# CREATING A TABLE AND ADDING IT TO THE SAME METADATA COLLECTION
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30), nullable=False),
    Column("fullname", String),
)

# CREATING ANOTHER TABLE WITH FOREIGNKEY

address_table = Table(
    "address",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False)
)

metadata_obj.create_all(engine)