from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Column, Field, SQLModel, String

from models.author import Author


class BookBase(SQLModel):
    title: str = Field(sa_column=Column("title", String, unique=True))
    author_id: UUID


class BookCreate(BookBase):
    pass


class BookUpdate(SQLModel):
    title: str | None = None
    author_id: UUID | None = None


class BookRead(BaseModel):
    id: UUID
    title: str
    author: Author | None
