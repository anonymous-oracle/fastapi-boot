from typing import List
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    title: str
    body: str

    # used to make pydantic schemas compatible with ORM models
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class ResponseUser(BaseModel):
    name: str
    email: str

    # initialize the relationship fields in a schema with proper datastructure
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class ResponseBlog(BaseModel):

    title: str
    user: ResponseUser

    class Config:
        orm_mode = True
