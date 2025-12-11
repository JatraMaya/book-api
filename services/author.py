from typing import Sequence
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_400_BAD_REQUEST
from models.author import Author
from repositories.author import AuthorRepo
from schemas.author import AuthorCreate, AuthorUpdate


class AuthorService:
    def __init__(self, repo: AuthorRepo):
        self.repo = repo

    def create_author(self, data: AuthorCreate) -> Author:
        try:
            author = Author(**data.model_dump())
            return self.repo.create(author)
        except IntegrityError as e:
            self.repo.session.rollback()
            self.handle_integrity_error(e)

    def get_author(self, author_id: UUID) -> Author:
        author = self.repo.get_by_id(author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
            )
        return author

    def get_all_authors(self) -> Sequence[Author]:
        return self.repo.get_all()

    def update_author(self, author_id: UUID, author: AuthorUpdate) -> Author:
        author_update = self.repo.update(
            author_id, author.model_dump(exclude_unset=True)
        )
        if not author_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
            )

        return author_update

    def delete_author(self, author_id: UUID) -> dict[str, str]:
        success = self.repo.delete(author_id)
        if not success:
            raise HTTPException(status_code=404, detail="Author not found")
        return {"detail": "Author with id: {author_id} is deleted succesfully"}

    def handle_integrity_error(self, error: IntegrityError):
        err_msg = str(error.orig).lower()

        if "name" in err_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exist"
            )
        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="Duplicate entry"
            )
