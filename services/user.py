from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models.user import User
from repositories.user import UserRepo
from schemas.user import UserCreate, UserRead

from core.utils import hash


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def create_user(self, data: UserCreate) -> UserRead:
        try:
            extra_data = {"password": hash(data.password)}
            user = User.model_validate(data, update=extra_data)
            created_user = self.repo.create_user(user)
            return self.convert_for_response(created_user)
        except IntegrityError as e:
            self.repo.session.rollback()
            self.handle_integrity_error(e)

    def get_all_users(self, limit: int, offset: int) -> Sequence[UserRead]:
        users = self.repo.get_users(offset, limit)
        return [
            UserRead(id=u.id, name=u.name, email=u.email, is_active=u.is_active)
            for u in users
        ]

    def get_user(self, user_id: UUID) -> UserRead:
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.model_validate(user)

    def delete_user(self, user_id: UUID) -> dict[str, str]:
        success = self.repo.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "Success"}

    def handle_integrity_error(self, error: IntegrityError):
        err_msg = str(error.orig).lower()

        if "email" in err_msg:
            raise HTTPException(status_code=400, detail="Email already exist")
        else:
            raise HTTPException(status_code=400, detail="Duplicate Entry")

    def convert_for_response(self, user: User) -> UserRead:
        return UserRead.model_validate(user)
