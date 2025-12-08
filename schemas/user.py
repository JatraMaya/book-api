from uuid import UUID

from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    email: EmailStr
    is_active: bool = True

    @field_validator("name")
    def name_validator(cls, v: str) -> str:
        v = v.strip()
        if len(v) <= 3:
            raise ValueError("Name must be atleast 3 characters or more")
        return v


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def password_validator(cls, v: str) -> str:
        if len(v) <= 5:
            raise ValueError("Password must be atleast six characters length")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Password must contain a special character")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a number")
        return v


class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]


class UserRead(UserBase):
    id: UUID


class AdminBase(SQLModel):
    pass


class AdminRead(AdminBase):
    id: int


class LoginRequest(SQLModel):
    email: EmailStr
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
