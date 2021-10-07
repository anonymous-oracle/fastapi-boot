from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str

    # used to make pydantic schemas compatible with ORM models
    class Config:
        orm_mode = True


class ResponseBlog(BaseModel):

    title: str

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

    class Config:
        orm_mode = True
