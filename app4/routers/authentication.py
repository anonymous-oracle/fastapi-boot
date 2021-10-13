from fastapi import APIRouter
from ..hashing import hash
from ..models import User, db
from ..schemas import Login, ResponseUser
from fastapi.exceptions import HTTPException

router = APIRouter(tags=["LOGIN"])


@router.post("/login", response_model=ResponseUser)
async def login(request: Login):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"invalid credentials",
        )
    if not hash.verify(request.password, user.password):
        raise HTTPException(status_code=404, detail=f"incorrect password")
    return user
