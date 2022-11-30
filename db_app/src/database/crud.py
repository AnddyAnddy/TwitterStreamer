from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.auth.password import get_hashed_password
from src.db_models.db_tweet import Tweet
from src.db_models.db_user import User


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def fetch_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_new_user(db: Session, user: User):
    password = get_hashed_password(user.password.encode())
    db_user = User(email=user.email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_new_tweet(db: Session, tweet: Tweet) -> Tweet | None:
    tweet = Tweet(tweet_id=tweet.tweet_id, author_id=tweet.author_id)
    try:
        db.add(tweet)
        db.commit()
        db.refresh(tweet)
        return tweet
    except IntegrityError:
        db.rollback()
        return None


def create_new_tweets(db: Session, tweets: list[Tweet]) -> list[Tweet]:
    tweets = [Tweet(tweet_id=tweet.tweet_id, author_id=tweet.author_id) for tweet in tweets]
    db.bulk_save_objects(tweets)
    db.commit()
    # db.refresh(tweets)
    return tweets


def get_all_tweets(db: Session, skip: int = 0, limit: int = 100) -> list[Tweet]:
    return db.query(Tweet).offset(skip).limit(limit).all()
