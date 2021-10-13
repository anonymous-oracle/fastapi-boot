from typing import List, Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class UserBase(BaseModel):
    name: str
    email: str
    password: str


class Blog(BlogBase):
    title: str
    body: str

    # used to make pydantic schemas compatible with ORM models
    class Config:
        orm_mode = True


class User(UserBase):
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
    user: ResponseUser = None

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class ResponseLogin(BaseModel):
    username: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
