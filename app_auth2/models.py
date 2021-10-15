from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE_URI = "sqlite:///./blog.db"

engine_ = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})


Base = declarative_base()
db = Session(bind=engine_, autocommit=False, autoflush=False)


# class Blog(Base):
#     __tablename__ = "blogs"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     body = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     # user = relationship("User", backref="users")
#     user = relationship("User", back_populates="blogs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    # blogs = relationship("Blog", back_populates="user")


if __name__ == "__main__":
    Base.metadata.create_all(engine_)
