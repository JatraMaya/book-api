from typing import Annotated, Sequence
from uuid import UUID
from fastapi import APIRouter, Depends

from core.depends import get_book_service, admin_required
from services.book import BookService
from schemas.book import BookCreate, BookRead, BookUpdate

public_router = APIRouter(prefix="/book", tags=["Book"])
admin_router = APIRouter(
    prefix="/book", tags=["Book"], dependencies=[Depends(admin_required)]
)


@public_router.get("/all", response_model=Sequence[BookRead])
def get_all_books(
    limit: Annotated[int, "Items limit to display"] = 10,
    offset: Annotated[int, "Offset limit to display"] = 0,
    service: BookService = Depends(get_book_service),
):
    return service.get_all_books(limit, offset)


@public_router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: UUID, service: BookService = Depends(get_book_service)):
    return service.get_book(book_id)


@admin_router.post("/", response_model=BookRead)
def create_book(data: BookCreate, service: BookService = Depends(get_book_service)):
    return service.create_book(data)


@admin_router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: UUID, data: BookUpdate, service: BookService = Depends(get_book_service)
):
    return service.update_book(book_id, data)


@admin_router.delete("/{book_id}")
def delete_book(book_id: UUID, service: BookService = Depends(get_book_service)):
    return service.delete_book(book_id)
