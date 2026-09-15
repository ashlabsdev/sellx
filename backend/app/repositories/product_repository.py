from sqlalchemy.orm import Session

from app.models.product import Product

def get_products(
    db: Session,
    search: str | None = None,
    category_id: int | None = None,
    status: str | None = None,
) -> list[Product]:
    query = db.query(Product)

    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    if category_id is not None:
        query = query.filter(
            Product.category_id == category_id
        )

    if status:
        query = query.filter(
            Product.status == status
        )

    return query.all()

def get_product_by_slug(
    db: Session,
    slug: str,
) -> Product | None:
    return (
        db.query(Product)
        .filter(Product.slug == slug)
        .first()
    )

def create_product(
    db: Session,
    product: Product,
) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def update_product(
    db: Session,
    product: Product,
) -> Product:
    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product: Product,
) -> None:
    db.delete(product)
    db.commit()