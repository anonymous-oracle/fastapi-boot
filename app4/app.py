from typing import List
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from .hashing import hash
from .schemas import *
from .database import db
from .routers import blog, user


app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
