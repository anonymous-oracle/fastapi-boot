from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE_URI = "sqlite:///./blog.db"

engine_ = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})


Base = declarative_base()

Base.metadata.create_all(engine_)

db = Session(bind=engine_, autocommit=False, autoflush=False)
