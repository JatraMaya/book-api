from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from models.book import Book


class BookRepo:
    def __init__(self, session: Session):
        self.session = session

    def create(self, book: Book) -> Book:
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def get_by_id(self, book_id: UUID) -> Optional[Book]:
        statement = (
            select(Book).where(Book.id == book_id).options(selectinload(Book.author))
        )
        return self.session.exec(statement).first()

    def get_by_author(self, author_id: UUID) -> Sequence[Book]:
        return self.session.exec(select(Book).where(Book.author_id == author_id)).all()

    def get_all(self, limit: int, offset: int) -> Sequence[Book]:
        statement = select(Book).offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def update(self, book_id: UUID, data: dict) -> Optional[Book]:
        book = self.get_by_id(book_id)

        if not book:
            return None

        for k, v in data.items():
            setattr(book, k, v)

        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def delete(self, book_id: UUID) -> bool:
        book = self.get_by_id(book_id)

        if not book:
            return False

        self.session.delete(book)
        self.session.commit()
        return True
