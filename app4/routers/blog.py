from fastapi import APIRouter
from typing import List

from fastapi.params import Depends
from app4.oauth2 import get_current_user

from app4.utils.blog import create_blog, destroy_blog, get_blog, update_blog
from .. import schemas, models

router = APIRouter(tags=["BLOGS"], prefix="/blog")


@router.get(
    "/",
    status_code=200,
    response_model=List[schemas.ResponseBlog],
)
# the Depends method will use the get_current_user to get the username of the current request
async def all(current_user: schemas.User = Depends(get_current_user)):
    return models.db.query(models.Blog).all()


@router.post(
    "/",
    status_code=201,
)
async def create(request: schemas.Blog):
    return await create_blog(title=request.title, body=request.body)


@router.get(
    "/{id}",
    status_code=200,
    response_model=schemas.ResponseBlog,
)
async def show(id):
    return await get_blog(id)


@router.delete(
    "/{id}",
    status_code=202,
)
async def delete_blog(id):
    return await destroy_blog(id)


@router.put(
    "/{id}",
    status_code=202,
)
async def update(id: int, request: schemas.Blog):
    return await update_blog(id, request.title, request.body)
