from typing import Optional, Sequence
from uuid import UUID
from sqlmodel import Session, select

from models.author import Author


class AuthorRepo:
    def __init__(self, session: Session):
        self.session = session

    def create(self, author: Author) -> Author:
        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)
        return author

    def get_by_id(self, author_id: UUID) -> Optional[Author]:
        return self.session.get(Author, author_id)

    def get_all(self) -> Sequence[Author]:
        return self.session.exec(select(Author)).all()

    def update(self, author_id: UUID, data: dict) -> Optional[Author]:
        author = self.get_by_id(author_id)

        if not author:
            return None

        for k, v in data.items():
            setattr(author, k, v)

        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)
        return author

    def delete(self, author_id: UUID) -> bool:
        author = self.get_by_id(author_id)
        if not author:
            return False

        self.session.delete(author)
        self.session.commit()
        return True
