from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.slug import generate_slug
from app.models.product import Product
from app.repositories.product_repository import (
    create_product,
    delete_product,
    get_product_by_slug,
    get_products,
    update_product,
)
from app.schemas.product import ProductCreate, ProductUpdate


def create_unique_slug(
    db: Session,
    name: str,
    current_product_id: int | None = None,
) -> str:
    base_slug = generate_slug(name)

    if not base_slug:
        base_slug = "product"

    slug = base_slug
    counter = 2

    while True:
        existing_product = get_product_by_slug(db, slug)

        if existing_product is None:
            return slug

        if (
            current_product_id is not None
            and existing_product.id == current_product_id
        ):
            return slug

        slug = f"{base_slug}-{counter}"
        counter += 1


def list_products(
    db: Session,
    search: str | None = None,
    category_id: int | None = None,
    status: str | None = None,
) -> list[Product]:
    return get_products(
        db,
        search=search,
        category_id=category_id,
        status=status,
    )


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

    slug = create_unique_slug(
        db,
        data.name,
    )

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


def edit_product(
    db: Session,
    product: Product,
    data: ProductUpdate,
) -> Product:
    product.name = data.name
    product.category_id = data.category_id
    product.description = data.description
    product.price = data.price
    product.condition = data.condition
    product.location = data.location
    product.contact_phone = data.contact_phone
    product.status = data.status

    product.slug = create_unique_slug(
        db,
        data.name,
        current_product_id=product.id,
    )

    product.updated_at = datetime.now(timezone.utc)

    return update_product(db, product)


def remove_product(
    db: Session,
    product: Product,
) -> None:
    delete_product(db, product)