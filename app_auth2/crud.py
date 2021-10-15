from models import db, User
from hashing import hash


async def read_user(**kwargs):
    id_ = kwargs.get("id")
    if id_ != None:
        return db.query(User).filter(User.id == id_).first()
    username = kwargs.get("username")
    if username != None:
        return db.query(User).filter(User.username == username).first()


async def create_user(username: str, password: str):
    new_user = User(username=username, password=hash(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
