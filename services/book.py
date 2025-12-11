from typing import Sequence
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from models.book import Book
from repositories.book import BookRepo
from repositories.author import AuthorRepo
from schemas.book import BookCreate, BookRead, BookUpdate


class BookService:
    def __init__(self, book_repo: BookRepo, author_repo: AuthorRepo):
        self.book_repo = book_repo
        self.author_repo = author_repo

    def create_book(self, data: BookCreate) -> BookRead:
        author = self.author_repo.get_by_id(data.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")

        book = Book(**data.model_dump())
        try:
            response_book = self.book_repo.create(book)
            return self.convert_for_response(response_book)
        except IntegrityError as e:
            if "UNIQUE constraint" in str(e.orig):
                raise HTTPException(status_code=409, detail="Book Already Exist")
            raise

    def get_book(self, book_id: UUID) -> BookRead:
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        return BookRead(id=book.id, author=book.author, title=book.title)

    def get_all_books(self, limit: int, offset: int) -> Sequence[BookRead]:
        result = self.book_repo.get_all(limit, offset)
        return [BookRead(id=b.id, title=b.title, author=b.author) for b in result]

    def get_by_author(self, author_id: UUID) -> Sequence[Book]:
        author = self.author_repo.get_by_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return self.book_repo.get_by_author(author_id)

    def update_book(self, book_id: UUID, book: BookUpdate) -> BookRead:
        # Validate author existance if it's also updated
        if book.author_id:
            author = self.author_repo.get_by_id(book.author_id)
            if not author:
                raise HTTPException(status_code=404, detail="Author not found")

        book_update = self.book_repo.update(
            book_id, book.model_dump(exclude_unset=True)
        )
        if not book_update:
            raise HTTPException(status_code=404, detail="Book not found")
        return self.convert_for_response(book_update)

    def delete_book(self, book_id: UUID):
        success = self.book_repo.delete(book_id)
        if not success:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"yey": "yey"}

    def convert_for_response(self, book: Book) -> BookRead:
        print(book)
        return BookRead(id=book.id, title=book.title, author=book.author)
