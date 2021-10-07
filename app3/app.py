from typing import List
from fastapi import FastAPI, status, Response
from fastapi.exceptions import HTTPException
from hashing import hash
import schemas
from models import Base, Blog, User
from database import engine_, session_

Base.metadata.create_all(engine_)

app = FastAPI()

db = session_


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["BLOGS"])
async def create(request: schemas.Blog):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get(
    "/blog",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ResponseBlog],
    tags=["BLOGS"],
)
async def all():
    return db.query(Blog).all()


@app.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseBlog,
    tags=["BLOGS"],
)
async def show(id, response: Response):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No blog with id: {id}"
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"No blog with id: {id}"}
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["BLOGS"])
async def delete_blog(id):
    db.query(Blog).filter(Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return True


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["BLOGS"])
async def update(id: int, request: schemas.Blog):
    blog = db.query(Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog not found for id: {id}"
        )
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return True


@app.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseUser,
    tags=["USERS"],
)
async def create_user(request: schemas.User):
    hashedPassword = hash.bcrypt_(request.password)
    new_user = User(name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model=schemas.ResponseUser, tags=["USERS"])
async def get_user(id: int):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found for id={id}"
        )
    return user
