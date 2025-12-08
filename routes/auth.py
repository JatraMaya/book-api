from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.depends import get_auth_service
from core.utils import produce_token
from schemas.user import Token
from services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    access_token = produce_token({"sub": user.email})
    return Token(access_token=access_token)
