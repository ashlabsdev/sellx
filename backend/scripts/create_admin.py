from datetime import datetime, timezone
from getpass import getpass

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.admin import Admin
from app.repositories.admin_repository import (
    create_admin,
    get_admin_by_email,
)


def main():
    email = input(
        "Admin email: "
    ).strip().lower()

    password = getpass(
        "Admin password: "
    )

    db = SessionLocal()

    try:
        existing_admin = get_admin_by_email(
            db,
            email,
        )

        if existing_admin:
            print(
                "Admin with this email already exists."
            )
            return

        admin = Admin(
            email=email,
            password_hash=hash_password(
                password
            ),
            is_active=True,
            created_at=datetime.now(
                timezone.utc
            ),
        )

        create_admin(
            db,
            admin,
        )

        print(
            f"Admin created successfully: {admin.email}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()