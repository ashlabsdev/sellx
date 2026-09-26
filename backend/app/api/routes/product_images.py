from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.security import get_current_admin
from app.models.admin import Admin

from app.schemas.product_image import (
    ProductImageReorder,
    ProductImageResponse,
    ProductImageUpdate,
)

from app.core.database import get_db

from app.services.product_image_service import (
    add_product_image,
    edit_product_image,
    get_product_image_by_id,
    list_product_images,
    remove_product_image,
    reorder_images,
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
    current_admin: Admin = Depends(
        get_current_admin
    ),
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
    current_admin: Admin = Depends(
        get_current_admin
    ),
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
    current_admin: Admin = Depends(
        get_current_admin
    ),
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
    current_admin: Admin = Depends(
        get_current_admin
    ),
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
    "/reorder",
    response_model=list[ProductImageResponse],
)
def reorder_product_images_route(
    product_id: int,
    data: ProductImageReorder,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    return reorder_images(
        db,
        product_id,
        data.image_ids,
    )


@router.put(
    "/{image_id}",
    response_model=ProductImageResponse,
)
def update_image(
    product_id: int,
    image_id: int,
    data: ProductImageUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    return edit_product_image(
        db,
        product_id=product_id,
        image_id=image_id,
        display_order=data.display_order,
        is_primary=data.is_primary,
    )

# 18.14 — Preview API endpoint
from app.schemas.image_processing import (
    ImageProcessRequest,
    ImageProcessResponse,
    ImageSaveRequest,
)

from app.services.image_editor_service import (
    create_image_preview,  save_edited_image,
)

@router.post(
    "/{image_id}/preview-edit",
    response_model=ImageProcessResponse,
)
def preview_image_edit(
    product_id: int,
    image_id: int,
    data: ImageProcessRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    return create_image_preview(
        db,
        product_id,
        image_id,
        data.background,
    )


# 18.17 — Save endpoint
@router.post(
    "/{image_id}/save-edit",
    response_model=ProductImageResponse,
)
def save_image_edit(
    product_id: int,
    image_id: int,
    data: ImageSaveRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    return save_edited_image(
        db,
        product_id,
        image_id,
        data.background,
    )
