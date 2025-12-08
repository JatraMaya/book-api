from fastapi import HTTPException, status
from pydantic import EmailStr, TypeAdapter, ValidationError
from repositories.user import UserRepo

from core.utils import verify
from schemas.user import UserRead


class AuthService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def authenticate_user(self, email: str, password: str) -> UserRead:
        try:
            email_adapter = TypeAdapter(EmailStr)
            validated_email = email_adapter.validate_python(email)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email Format"
            )

        user = self.repo.get_user_by_email(str(validated_email))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        password_valid = verify(password, user.password)
        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        return UserRead.model_validate(user)
