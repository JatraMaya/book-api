from uuid import UUID, uuid4
from pydantic import EmailStr


from sqlmodel import Column, Field, Relationship, String
from schemas.user import AdminBase, UserBase


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False, index=True)
    password: str = Field(sa_column=Column("hashed_password", String, nullable=False))
    email: EmailStr = Field(index=True, unique=True, nullable=False)


class Admin(AdminBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", unique=True, index=True)
    user: User = Relationship()
