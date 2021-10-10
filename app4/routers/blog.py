from fastapi import APIRouter
from typing import List
from fastapi import status, Response, HTTPException
from .. import database, schemas, models

router = APIRouter(tags=["BLOGS"], prefix="/blog")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ResponseBlog],
)
async def all():
    return database.db.query(models.Blog).all()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(request: schemas.Blog):
    new_blog = schemas.Blog(title=request.title, body=request.body, user_id=1)
    database.db.add(new_blog)
    database.db.commit()
    database.db.refresh(new_blog)
    return new_blog


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseBlog,
)
async def show(id, response: Response):
    blog = database.db.query(database.Blog).filter(database.Blog.id == id).first()
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
    database.db.query(database.Blog).filter(database.Blog.id == id).delete(
        synchronize_session=False
    )
    database.db.commit()
    return True


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def update(id: int, request: schemas.Blog):
    blog = database.db.query(database.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog not found for id: {id}"
        )
    blog.update({"title": request.title, "body": request.body})
    database.db.commit()
    return True
