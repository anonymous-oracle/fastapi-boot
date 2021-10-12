from fastapi import APIRouter
from typing import List
from fastapi import status, HTTPException
from .. import schemas, models

router = APIRouter(tags=["USERS"], prefix='/user')


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseUser,
)
async def create_user(request: schemas.User):
    hashedPassword = hash.bcrypt_(request.password)
    new_user = models.User(
        name=request.name, email=request.email, password=hashedPassword
    )
    models.db.add(new_user)
    models.db.commit()
    models.db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.ResponseUser)
async def get_user(id: int):
    user = models.db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found for id={id}"
        )
    return user
