from sqlalchemy import Table, Column, ForeignKey, Integer, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql:///:memory:", future=True)
conn = engine.connect()

conn.close()
