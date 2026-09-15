from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.slug import generate_slug
from app.models.category import Category
from app.repositories.category_repository import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    get_category_by_slug,
    update_category,
)
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


def create_unique_category_slug(
    db: Session,
    name: str,
    current_category_id: int | None = None,
) -> str:
    base_slug = generate_slug(name)

    if not base_slug:
        base_slug = "category"

    slug = base_slug
    counter = 2

    while True:
        existing_category = get_category_by_slug(
            db,
            slug,
        )

        if existing_category is None:
            return slug

        if (
            current_category_id is not None
            and existing_category.id == current_category_id
        ):
            return slug

        slug = f"{base_slug}-{counter}"
        counter += 1


def list_categories(
    db: Session,
) -> list[Category]:
    return get_categories(db)


def get_category_by_id(
    db: Session,
    category_id: int,
) -> Category | None:
    return get_category(db, category_id)


def add_category(
    db: Session,
    data: CategoryCreate,
) -> Category:
    now = datetime.now(timezone.utc)

    slug = create_unique_category_slug(
        db,
        data.name,
    )

    category = Category(
        name=data.name,
        slug=slug,
        description=data.description,
        is_active=True,
        created_at=now,
        updated_at=now,
    )

    return create_category(
        db,
        category,
    )


def edit_category(
    db: Session,
    category: Category,
    data: CategoryUpdate,
) -> Category:
    category.name = data.name
    category.description = data.description
    category.is_active = data.is_active

    category.slug = create_unique_category_slug(
        db,
        data.name,
        current_category_id=category.id,
    )

    category.updated_at = datetime.now(timezone.utc)

    return update_category(
        db,
        category,
    )


def remove_category(
    db: Session,
    category: Category,
) -> None:
    delete_category(
        db,
        category,
    )