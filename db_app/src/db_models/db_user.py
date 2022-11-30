from sqlalchemy import Column, Integer, String, Sequence

from src.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
