from sqlalchemy.orm import Session

from app.models.product_image import ProductImage


def get_product_images(
    db: Session,
    product_id: int,
) -> list[ProductImage]:
    return (
        db.query(ProductImage)
        .filter(
            ProductImage.product_id == product_id
        )
        .order_by(
            ProductImage.display_order
        )
        .all()
    )


def get_product_image(
    db: Session,
    image_id: int,
) -> ProductImage | None:
    return (
        db.query(ProductImage)
        .filter(
            ProductImage.id == image_id
        )
        .first()
    )


def create_product_image(
    db: Session,
    image: ProductImage,
) -> ProductImage:
    db.add(image)
    db.commit()
    db.refresh(image)

    return image


def update_product_image(
    db: Session,
    image: ProductImage,
) -> ProductImage:
    db.commit()
    db.refresh(image)

    return image


def delete_product_image(
    db: Session,
    image: ProductImage,
) -> None:
    db.delete(image)
    db.commit()