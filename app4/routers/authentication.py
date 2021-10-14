from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..tokenJWT import create_access_token
from ..hashing import hash
from ..models import User, db
from ..schemas import Token
from fastapi.exceptions import HTTPException

router = APIRouter(tags=["LOGIN"])


@router.post("/login", response_model=Token)
async def login(request: OAuth2PasswordRequestForm=Depends()):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"invalid credentials",
        )
    if not hash.verify(request.password, user.password):
        raise HTTPException(status_code=404, detail=f"incorrect password")

    # creating the access token
    # after validating the credentials and the password, we create a token based on the username of the User stored in the database and sign it
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
