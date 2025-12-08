from uuid import UUID, uuid4
from sqlmodel import Field, Relationship


from models.author import Author
from schemas.book import BookBase


class Book(BookBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    author_id: UUID = Field(foreign_key="author.id")
    author: "Author" = Relationship(back_populates="books")
