from typing import List
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from .hashing import hash
from .schemas import *
from .models import db, Base, engine_
from .routers import blog, user



app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
