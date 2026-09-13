from sqlalchemy.orm import Session

from app.models.product import Product


def get_products(db: Session) -> list[Product]:
    return db.query(Product).all()


def get_product(
    db: Session,
    product_id: int,
) -> Product | None:
    return (
        db.query(Product)
        .filter(Product.id == product_id)
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