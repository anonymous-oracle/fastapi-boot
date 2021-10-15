from fastapi import FastAPI, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from crud import create_user, read_user
from auth import get_current_user, get_token, authenticate_user, HTTPException
from schemas import User, UserResponse


app = FastAPI()


@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if user == False:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    user_obj = {"id": user.id, "username": user.username}
    return get_token(user_obj)


@app.post("/users", response_model=UserResponse)
async def post_user(user: User):
    return await create_user(username=user.username, password=user.password)


@app.get("/users/me", response_model=UserResponse)
async def get_user_me(user: User = Depends(get_current_user)):
    return user


@app.get("/users/{username}", response_model=UserResponse)
async def get_user(username: str):
    return await read_user(username=username)
