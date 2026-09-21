from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.repositories.admin_repository import (
    get_admin_by_email,
)
from app.core.security import verify_password


def authenticate_admin(
    db: Session,
    email: str,
    password: str,
) -> Admin:
    admin = get_admin_by_email(
        db,
        email,
    )

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        password,
        admin.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive",
        )

    return admin