from fastapi import APIRouter
from typing import List
from fastapi import status, Response, HTTPException

from app4.utils.blog import create_blog, destroy_blog
from .. import schemas, models

router = APIRouter(tags=["BLOGS"], prefix="/blog")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ResponseBlog],
)
async def all():
    return models.db.query(models.Blog).all()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(request: schemas.Blog):
    return create_blog(title=request.title, body=request.body)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseBlog,
)
async def show(id, response: Response):
    blog = models.db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No blog with id: {id}"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"No blog with id: {id}"}
    return blog


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_blog(id):
    return destroy_blog(id)


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def update(id: int, request: schemas.Blog):
    blog = models.db.query(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog not found for id: {id}"
        )
    blog.update({"title": request.title, "body": request.body})
    models.db.commit()
    return True
