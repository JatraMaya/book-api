from typing import Annotated, Sequence
from uuid import UUID
from fastapi import APIRouter, Depends

from schemas.user import UserCreate, UserRead
from services.user import UserService

from core.depends import get_user_service


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserRead)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(data)


@router.get("/all", response_model=Sequence[UserRead])
def get_all_users(
    limit: Annotated[int, "List limit to display"] = 10,
    offset: Annotated[int, "Offset limit to display"] = 0,
    service: UserService = Depends(get_user_service),
):
    return service.get_all_users(limit, offset)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    return service.get_user(user_id)


@router.delete("/{user_id}")
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    return service.delete_user(user_id)
