from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.db import get_session

from core.utils import decode_token
from repositories.author import AuthorRepo
from repositories.book import BookRepo
from repositories.user import UserRepo

from services.auth import AuthService
from services.author import AuthorService
from services.book import BookService
from services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_user_repo(session: Session = Depends(get_session)):
    return UserRepo(session)


def get_author_repo(session: Session = Depends(get_session)):
    return AuthorRepo(session)


def get_book_repo(session: Session = Depends(get_session)):
    return BookRepo(session)


def get_auth_service(repo: UserRepo = Depends(get_user_repo)):
    return AuthService(repo)


def get_author_service(repo: AuthorRepo = Depends(get_author_repo)):
    return AuthorService(repo)


def get_book_service(
    book_repo: BookRepo = Depends(get_book_repo),
    author_repo: AuthorRepo = Depends(get_author_repo),
):
    return BookService(book_repo, author_repo)


def get_user_service(repo: UserRepo = Depends(get_user_repo)):
    return UserService(repo)


# Auth Related dependency
def get_current_user(
    token: str = Depends(oauth2_scheme), repo: UserRepo = Depends(get_user_repo)
):
    payload = decode_token(token)
    email = payload.get("sub")
    user = repo.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User unauthorized"
        )
    return user


def admin_required(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    repo = UserRepo(session)
    if not repo.verify_is_admin(current_user.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User unauthorized"
        )
    return None
