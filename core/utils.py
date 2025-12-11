import jwt
import logging
from fastapi import HTTPException, status
from datetime import timedelta, datetime, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from core.config import get_settings

settings = get_settings()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger(__name__)

password_hash = PasswordHash.recommended()


def hash(password: str) -> str:
    return password_hash.hash(password)


def verify(password: str, hash_password: str) -> bool:
    return password_hash.verify(password, hash_password)


def produce_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    return encoded_jwt


def decode_token(token: str):
    try:
        decode = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return decode
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unhandled Exception: {e}",
        )
