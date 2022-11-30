from fastapi import Depends, APIRouter, HTTPException
from requests import Session

from src.database import crud
from src.database.database import SessionLocal, engine
from src.db_models import db_user
from src.models.tweet import Tweet

db_user.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix='/tweets')


# Dependency
def get_db():
    db: SessionLocal = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/", response_model=Tweet)
def create_tweet(tweet: Tweet, db: Session = Depends(get_db)):
    print(tweet)
    tweet: Tweet | None = crud.create_new_tweet(db=db, tweet=tweet)
    if tweet is None:
        raise HTTPException(status_code=404, detail="Tweet already exists")
    return tweet


@router.post("/tweets", response_model=list[Tweet])
def create_tweet(tweets: list[Tweet], db: Session = Depends(get_db)):
    return crud.create_new_tweets(db=db, tweets=tweets)


@router.get("/", response_model=list[Tweet])
def read_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tweets = crud.get_all_tweets(db, skip=skip, limit=limit)
    return tweets
