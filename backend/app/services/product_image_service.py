from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product_image import ProductImage
from app.repositories.product_image_repository import (
    create_product_image,
    delete_product_image,
    get_product_image,
    get_product_images,
    reorder_product_images,
    update_product_image,
)
from app.repositories.product_repository import (
    get_product,
)

def reorder_images(
    db: Session,
    product_id: int,
    image_ids: list[int],
) -> list[ProductImage]:
    existing_images = list_product_images(
        db,
        product_id,
    )

    existing_ids = {
        image.id
        for image in existing_images
    }

    requested_ids = set(image_ids)

    if len(image_ids) != len(requested_ids):
        raise HTTPException(
            status_code=400,
            detail="Image IDs must not contain duplicates",
        )

    if requested_ids != existing_ids:
        raise HTTPException(
            status_code=400,
            detail=(
                "Image IDs must include all images "
                "belonging to this product"
            ),
        )

    images_by_id = {
        image.id: image
        for image in existing_images
    }

    ordered_images = [
        images_by_id[image_id]
        for image_id in image_ids
    ]

    return reorder_product_images(
        db,
        ordered_images,
    )


def list_product_images(
    db: Session,
    product_id: int,
) -> list[ProductImage]:
    product = get_product(
        db,
        product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return get_product_images(
        db,
        product_id,
    )


def get_product_image_by_id(
    db: Session,
    product_id: int,
    image_id: int,
) -> ProductImage:
    product = get_product(
        db,
        product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    image = get_product_image(
        db,
        image_id,
    )

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="Product image not found",
        )

    if image.product_id != product_id:
        raise HTTPException(
            status_code=404,
            detail="Product image not found",
        )

    return image


def add_product_image(
    db: Session,
    product_id: int,
    storage_path: str,
    image_url: str,
    display_order: int,
    is_primary: bool,
) -> ProductImage:
    product = get_product(
        db,
        product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    if is_primary:
        existing_images = get_product_images(
            db,
            product_id,
        )

        for image in existing_images:
            image.is_primary = False

    now = datetime.now(timezone.utc)

    image = ProductImage(
        product_id=product_id,
        storage_path=storage_path,
        image_url=image_url,
        display_order=display_order,
        is_primary=is_primary,
        created_at=now,
    )

    return create_product_image(
        db,
        image,
    )

def edit_product_image(
    db: Session,
    product_id: int,
    image_id: int,
    display_order: int | None = None,
    is_primary: bool | None = None,
) -> ProductImage:
    image = get_product_image_by_id(
        db,
        product_id,
        image_id,
    )

    if is_primary is True:
        existing_images = get_product_images(
            db,
            product_id,
        )

        for existing_image in existing_images:
            if existing_image.id != image_id:
                existing_image.is_primary = False

    if display_order is not None:
        image.display_order = display_order

    if is_primary is not None:
        image.is_primary = is_primary

    return update_product_image(
        db,
        image,
    )

def remove_product_image(
    db: Session,
    product_id: int,
    image_id: int,
) -> None:
    image = get_product_image_by_id(
        db,
        product_id,
        image_id,
    )

    was_primary = image.is_primary

    delete_product_image(
        db,
        image,
    )

    if not was_primary:
        return

    remaining_images = get_product_images(
        db,
        product_id,
    )

    if not remaining_images:
        return

    new_primary = remaining_images[0]
    new_primary.is_primary = True

    update_product_image(
        db,
        new_primary,
    )