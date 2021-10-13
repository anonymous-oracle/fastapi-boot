from fastapi import FastAPI
from .routers.blog import router as blog_router
from .routers.user import router as user_router
from .routers.authentication import router as auth_router


app = FastAPI()
app.include_router(blog_router)
app.include_router(user_router)
app.include_router(auth_router)
