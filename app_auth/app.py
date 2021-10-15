from fastapi import FastAPI
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


app = FastAPI()

# tokenUrl is an endpoint that generates a token for us
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @app.post('/token')
# # can directly get username and password
# def token(username:str, password:str):


@app.post("/token")
# form_data depends only on the OAuth2PasswordRequestForm and if there is any error, no token will be returned
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username + "token"}


@app.get("/")
# oauth2_scheme return a token if it is available
# also whatever endpoint/route depends on oauth2_scheme will require authorization
async def index(token: str = Depends(oauth2_scheme)):
    return {"token": token}
