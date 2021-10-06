from fastapi import FastAPI, status, Response
from fastapi.exceptions import HTTPException

import schemas
from models import Base, Blog
from database import engine_, session_

Base.metadata.create_all(engine_)

app = FastAPI()

db = session_()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", status_code=status.HTTP_200_OK)
async def all():
    blogs = db.query(Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
async def show(id, response: Response):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No blog with id: {id}"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"No blog with id: {id}"}
    return
