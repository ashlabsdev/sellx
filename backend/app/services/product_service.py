from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.slug import generate_slug
from app.models.product import Product
from app.repositories.product_repository import (
    create_product,
    delete_product,
    get_product,
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
    page: int = 1,
    page_size: int = 12,
) -> list[Product]:
    return get_products(
        db,
        search=search,
        category_id=category_id,
        status=status,
        page=page,
        page_size=page_size,
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

def validate_product_for_publish(
    product: Product,
) -> None:
    errors: list[str] = []

    if (
        not product.name
        or not product.name.strip()
    ):
        errors.append(
            "Product name is required"
        )

    if product.price <= 0:
        errors.append(
            "Price must be greater than 0"
        )

    if (
        not product.condition
        or not product.condition.strip()
    ):
        errors.append(
            "Condition is required"
        )

    if product.category is None:
        errors.append(
            "Category is required"
        )
    elif not product.category.is_active:
        errors.append(
            "Category must be active"
        )

    if (
        not product.description
        or not product.description.strip()
    ):
        errors.append(
            "Description is required"
        )

    if (
        not product.location
        or not product.location.strip()
    ):
        errors.append(
            "Location is required"
        )

    if (
        not product.contact_phone
        or not product.contact_phone.strip()
    ):
        errors.append(
            "Contact phone is required"
        )

    if not product.images:
        errors.append(
            "At least one product image is required"
        )

    elif not any(
        image.is_primary
        for image in product.images
    ):
        errors.append(
            "A primary product image is required"
        )

    if errors:
        raise HTTPException(
            status_code=400,
            detail={
                "message":
                    "Product cannot be published",
                "errors": errors,
            },
        )
    
def edit_product(
    db: Session,
    product: Product,
    data: ProductUpdate,
) -> Product:
    previous_status = product.status

    allowed_statuses = {
        "draft",
        "active",
        "sold",
    }

    if data.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid product status",
        )

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

    product.updated_at = datetime.now(
        timezone.utc
    )

    if (
        data.status == "active"
        and previous_status != "active"
    ):
        db.flush()

        validate_product_for_publish(
            product
        )

    return update_product(
        db,
        product,
    )

def remove_product(
    db: Session,
    product: Product,
) -> None:
    delete_product(db, product)