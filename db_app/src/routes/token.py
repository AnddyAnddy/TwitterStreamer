import binascii
import os

from fastapi import APIRouter, Depends

from src.auth.auth_bearer import JWTBearer

router = APIRouter(prefix='/token')


@router.get("/get_token", dependencies=[Depends(JWTBearer())])
def generate_token():
    """Get an unique token, you must submit a valid authentication token by login in."""
    token: str = _generate_token()
    return token


def _generate_token(length: int = 7) -> str:
    return binascii.hexlify(os.urandom(length)).decode()
