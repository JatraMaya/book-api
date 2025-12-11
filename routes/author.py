from typing import Sequence
from uuid import UUID
from fastapi import APIRouter, Depends, status

from schemas.author import AuthorCreate, AuthorRequest, AuthorUpdate
from core.depends import admin_required, get_author_service
from services.author import AuthorService


public_router = APIRouter(prefix="/author", tags=["Author"])
admin_router = APIRouter(
    prefix="/author", tags=["Author"], dependencies=[Depends(admin_required)]
)


@public_router.get("/all", response_model=Sequence[AuthorRequest])
def get_all_authors(
    service: AuthorService = Depends(get_author_service),
):
    return service.get_all_authors()


@public_router.get("/{author_id}", response_model=AuthorRequest)
def get_author(author_id: UUID, service: AuthorService = Depends(get_author_service)):
    return service.get_author(author_id)


@admin_router.post("/", response_model=AuthorRequest)
def create_author(
    data: AuthorCreate,
    service: AuthorService = Depends(get_author_service),
):
    return service.create_author(data)


@admin_router.put("/{author_id}", response_model=AuthorRequest)
def update_author(
    author_id: UUID,
    data: AuthorUpdate,
    service: AuthorService = Depends(get_author_service),
):
    return service.update_author(author_id, data)


@admin_router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Successfully deleted Author from system"},
        401: {
            "description": "Unauthorized - Authentication required",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
        403: {
            "description": "Forbidden - Required Admin access",
            "content": {
                "application/json": {"example": {"detail": "User Unauthorized"}}
            },
        },
        404: {
            "description": "Non existing record",
            "content": {
                "application/json": {"example": {"detail": "Author not found"}}
            },
        },
    },
)
def delete_author(
    author_id: UUID,
    service: AuthorService = Depends(get_author_service),
):
    service.delete_author(author_id)
