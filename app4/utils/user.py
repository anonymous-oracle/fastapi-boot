from fastapi.exceptions import HTTPException
from fastapi import status
from ..models import db, User
from ..hashing import hash

async def create_user(name:str, email:str, password:str):
    hashedPassword = hash.bcrypt_(password)
    new_user = User(
        name=name, email=email, password=hashedPassword
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def get_user(id: int):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found for id: {id}"
        )
    return user