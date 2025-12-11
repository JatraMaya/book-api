import uuid
from sqlmodel import Field, Relationship
from schemas.author import AuthorBase


class Author(AuthorBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    books: list["Book"] = Relationship(back_populates="author")
