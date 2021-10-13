from fastapi import APIRouter

from app4.utils.user import create_user, get_user
from .. import schemas, models

router = APIRouter(tags=["USERS"], prefix="/user")


@router.post(
    "/",
    status_code=201,
    response_model=schemas.ResponseUser,
)
async def create(request: schemas.User):
    return await create_user(name=request.name, email=request.email, password=request.password)


@router.get("/{id}", response_model=schemas.ResponseUser, status_code=200)
async def find_user(id: int):
    return await get_user(id)
