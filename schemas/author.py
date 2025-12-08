from uuid import UUID
from sqlmodel import SQLModel


class AuthorBase(SQLModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(SQLModel):
    name: str | None


class AuthorRequest(AuthorBase):
    id: UUID
