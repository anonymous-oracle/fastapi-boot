from fastapi.exceptions import HTTPException
from ..schemas import Blog
from ..models import Blog, db
from fastapi import status

# def create_blog(title: str, body: str, user_id: int):
async def create_blog(title: str, body: str):
    new_blog = Blog(title=title, body=body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


async def destroy_blog(id: int):
    blog = db.query(Blog).filter(Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"no blog with id: {id}"
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"


async def update_blog(id: int, title: str, body: str):
    blog = db.query(Blog).filter(Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog not found for id: {id}"
        )
    blog.update({"title": title, "body": body})
    db.commit()
    return "updated"


async def get_blog(id: int):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No blog with id: {id}"
        )
    return blog
