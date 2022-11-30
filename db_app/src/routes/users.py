from fastapi import Depends, APIRouter, HTTPException, Body
from requests import Session

from src.auth.auth_handler import signJWT
from src.auth.password import check_password
from src.database import crud
from src.database.database import SessionLocal, engine
from src.db_models import db_user
from src.models.model import User, Token

db_user.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix='/users')


# Dependency
def get_db():
    db: SessionLocal = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    users = crud.fetch_user_by_email(db, email=user.email)
    if users:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_new_user(db=db, user=user)


@router.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/login", response_model=Token)
async def user_login(user: User = Body(...), db: Session = Depends(get_db)):
    if check_user(db, user):
        return Token(access_token=signJWT(user.email)["access_token"])
    raise HTTPException(status_code=404, detail="Wrong login details")


def check_user(session: Session, data: User) -> bool:
    user = crud.fetch_user_by_email(session, data.email)
    res = check_password(data.password.encode(), user.password.encode())
    return res
