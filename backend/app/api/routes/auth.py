from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_current_admin,
)
from app.models.admin import Admin
from app.schemas.admin import AdminResponse

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)
from app.services.auth_service import (
    authenticate_admin,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.get(
    "/me",
    response_model=AdminResponse,
)
def get_me(
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    return current_admin



@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    admin = authenticate_admin(
        db,
        email=data.email.strip().lower(),
        password=data.password,
    )

    access_token = create_access_token(
        admin.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }