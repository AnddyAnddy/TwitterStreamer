from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "sample_email@example.com",
                "password": "sample_password"
            }
        }
        orm_mode = True


class TokenPayload(BaseModel):
    user_id: str = Field(...)
    expires: str = Field(...)


class Token(BaseModel):
    access_token: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "access_token": "example_access_token"
            }
        }
        orm_mode = True
