from sqlalchemy import Column, String

from src.database.database import Base


class Tweet(Base):
    __tablename__ = "tweet"

    author_id = Column(String, index=True)
    tweet_id = Column(String, unique=True, primary_key=True)
