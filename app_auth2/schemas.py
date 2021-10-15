from pydantic import BaseModel


class BaseUser(BaseModel):
    class Config:
        orm_mode = True


class User(BaseUser):
    username: str
    password: str


class UserResponse(BaseUser):
    id: int
    username: str
