from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import (
    create_product,
    get_product,
    get_products,
)
from app.schemas.product import ProductCreate


def list_products(db: Session) -> list[Product]:
    return get_products(db)


def get_product_by_id(
    db: Session,
    product_id: int,
) -> Product | None:
    return get_product(db, product_id)


def add_product(
    db: Session,
    data: ProductCreate,
) -> Product:
    now = datetime.now(timezone.utc)

    slug = data.name.strip().lower().replace(" ", "-")

    product = Product(
        name=data.name,
        slug=slug,
        category_id=data.category_id,
        description=data.description,
        price=data.price,
        condition=data.condition,
        location=data.location,
        contact_phone=data.contact_phone,
        status="draft",
        created_at=now,
        updated_at=now,
    )

    return create_product(db, product)