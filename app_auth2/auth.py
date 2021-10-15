from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from fastapi.exceptions import HTTPException
from hashing import verify
from crud import read_user


# `openssl rand -hex 32` -> to generate the secret
JWT_SECRET_KEY = "ca0264b9fbc96884dc27b5d09c1b480f53f43c178c9947c4bd05f3c49b77034b"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(username: str, password: str):
    user = await read_user(username=username)
    if user == None:
        return False
    if verify(password, user.password) == False:
        return False
    return user


def get_token(payload: dict):
    """payload: must be a dict object"""
    token = jwt.encode(payload=payload, key=JWT_SECRET_KEY)
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=["HS256"])
        user = await read_user(id=payload.get("id"))
    except:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user