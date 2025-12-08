from typing import Sequence
from uuid import UUID

from fastapi import HTTPException
from models.author import Author
from repositories.author import AuthorRepo
from schemas.author import AuthorCreate, AuthorUpdate


class AuthorService:
    def __init__(self, author_repo: AuthorRepo):
        self.author_repo = author_repo

    def create_author(self, data: AuthorCreate) -> Author:
        author = Author(**data.model_dump())
        return self.author_repo.create(author)

    def get_author(self, author_id: UUID) -> Author:
        author = self.author_repo.get_by_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    def get_all_authors(self) -> Sequence[Author]:
        return self.author_repo.get_all()

    def update_author(self, author_id: UUID, author: AuthorUpdate) -> Author:
        author_update = self.author_repo.update(
            author_id, author.model_dump(exclude_unset=True)
        )
        if not author_update:
            raise HTTPException(status_code=404, detail="Author not found")

        return author_update

    def delete_author(self, author_id: UUID):
        success = self.author_repo.delete(author_id)
        if not success:
            raise HTTPException(status_code=404, detail="Author not found")
