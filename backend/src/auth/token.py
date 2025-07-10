from datetime import datetime, timedelta
from typing import Optional

import jwt
from auth.exceptions import ExpiredTokenException, InvalidTokenException
from config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/token")


def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.auth.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.auth.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.auth.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.auth.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.InvalidTokenError:
        raise InvalidTokenException()
