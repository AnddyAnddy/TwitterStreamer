from pydantic import BaseModel, Field


class Tweet(BaseModel):
    tweet_id: str = Field(...)
    author_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "tweet_id": "12345",
                "author_id": "8189150"
            }
        }
        orm_mode = True
