from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE_URI = "sqlite:///./blog.db"

engine_ = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})

session_ = Session(bind=engine_, autocommit=False, autoflush=False)

Base = declarative_base()
