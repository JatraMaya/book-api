from typing import Optional, Sequence
from uuid import UUID
from sqlmodel import Session, select

from models.user import Admin, User


class UserRepo:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_users(self, offset: int, limit: int) -> Sequence[User]:
        statement = select(User).offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def get_user_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def verify_is_admin(self, email: str) -> bool:
        user = self.get_user_by_email(email)
        if not user:
            return False
        statement = select(Admin).where(Admin.user_id == user.id)
        admin = self.session.exec(statement).first()
        if not admin:
            return False
        return True

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return self.session.get(User, user_id)

    def delete_user(self, user_id: UUID) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True
