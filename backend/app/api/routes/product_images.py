from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product_image import ProductImageResponse
from app.services.product_image_service import (
    add_product_image,
    edit_product_image,
    get_product_image_by_id,
    list_product_images,
    remove_product_image,
)
from app.services.storage_service import (
    delete_product_image_file,
    upload_product_image,
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


@router.delete(
    "/{image_id}",
)
def delete_image(
    product_id: int,
    image_id: int,
    db: Session = Depends(get_db),
):
    image = get_product_image_by_id(
        db,
        product_id,
        image_id,
    )

    delete_product_image_file(
        image.storage_path
    )

    remove_product_image(
        db,
        product_id,
        image_id,
    )

    return {
        "message": "Product image deleted successfully",
    }


@router.post(
    "/upload",
    response_model=ProductImageResponse,
)
async def upload_image(
    product_id: int,
    file: UploadFile = File(...),
    display_order: int = Form(0),
    is_primary: bool = Form(False),
    db: Session = Depends(get_db),
):
    storage_path, image_url = await upload_product_image(
        product_id=product_id,
        file=file,
    )

    return add_product_image(
        db,
        product_id=product_id,
        storage_path=storage_path,
        image_url=image_url,
        display_order=display_order,
        is_primary=is_primary,
    )
@router.post(
    "/upload-multiple",
    response_model=list[ProductImageResponse],
)
async def upload_multiple_images(
    product_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    uploaded_images = []

    existing_images = list_product_images(
        db,
        product_id,
    )

    starting_display_order = len(existing_images)

    for index, file in enumerate(files):
        storage_path, image_url = await upload_product_image(
            product_id=product_id,
            file=file,
        )

        image = add_product_image(
            db,
            product_id=product_id,
            storage_path=storage_path,
            image_url=image_url,
            display_order=starting_display_order + index,
            is_primary=False,
        )

        uploaded_images.append(image)

    return uploaded_images


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
