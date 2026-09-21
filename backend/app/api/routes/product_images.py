from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product_image import ProductImageResponse
from app.services.product_image_service import (
    add_product_image,
    edit_product_image,
    list_product_images,
    remove_product_image,
)

router = APIRouter(
    prefix="/api/products/{product_id}/images",
    tags=["Product Images"],
)


@router.get(
    "",
    response_model=list[ProductImageResponse],
)
def get_images(
    product_id: int,
    db: Session = Depends(get_db),
):
    return list_product_images(
        db,
        product_id,
    )


@router.post(
    "",
    response_model=ProductImageResponse,
)
def create_image(
    product_id: int,
    storage_path: str,
    image_url: str,
    display_order: int = 0,
    is_primary: bool = False,
    db: Session = Depends(get_db),
):
    return add_product_image(
        db,
        product_id=product_id,
        storage_path=storage_path,
        image_url=image_url,
        display_order=display_order,
        is_primary=is_primary,
    )


@router.put(
    "/{image_id}",
    response_model=ProductImageResponse,
)
def update_image(
    product_id: int,
    image_id: int,
    storage_path: str,
    image_url: str,
    display_order: int = 0,
    is_primary: bool = False,
    db: Session = Depends(get_db),
):
    return edit_product_image(
        db,
        product_id=product_id,
        image_id=image_id,
        storage_path=storage_path,
        image_url=image_url,
        display_order=display_order,
        is_primary=is_primary,
    )


@router.delete(
    "/{image_id}",
)
def delete_image(
    product_id: int,
    image_id: int,
    db: Session = Depends(get_db),
):
    remove_product_image(
        db,
        product_id,
        image_id,
    )

    return {
        "message": "Product image deleted successfully",
    }