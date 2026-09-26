# 18.13 — Create processing service
import base64

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product_image import (
    ProductImage,
)

from app.services.image_processing.image_processor import (
    process_product_image,
)

from app.services.product_image_service import (
    get_product_image_by_id,
)

from app.services.storage_service import (
    delete_product_image_file,
    download_product_image_file,
    upload_processed_product_image,
)

from app.repositories.product_image_repository import (
    update_product_image,
)

def create_image_preview(
    db: Session,
    product_id: int,
    image_id: int,
    background: str,
) -> dict[str, str]:
    image = get_product_image_by_id(
        db,
        product_id,
        image_id,
    )

    original_bytes = (
        download_product_image_file(
            image.storage_path
        )
    )

    try:
        processed_bytes = (
            process_product_image(
                original_bytes,
                background,
            )
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    encoded_image = (
        base64.b64encode(
            processed_bytes
        ).decode("utf-8")
    )

    return {
        "image_base64":
            encoded_image,
        "content_type":
            "image/webp",
    }

# 18.16 — Save edited image service
def save_edited_image(
    db: Session,
    product_id: int,
    image_id: int,
    background: str,
) -> ProductImage:
    image = get_product_image_by_id(
        db,
        product_id,
        image_id,
    )

    old_storage_path = (
        image.storage_path
    )

    original_bytes = (
        download_product_image_file(
            old_storage_path
        )
    )

    try:
        processed_bytes = (
            process_product_image(
                original_bytes,
                background,
            )
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    new_storage_path = None

    try:
        (
            new_storage_path,
            new_image_url,
        ) = upload_processed_product_image(
            product_id,
            processed_bytes,
        )

        image.storage_path = (
            new_storage_path
        )

        image.image_url = (
            new_image_url
        )

        updated_image = (
            update_product_image(
                db,
                image,
            )
        )

    except Exception:
        # If upload succeeded but the DB
        # update failed, don't leave an
        # orphaned processed file.
        if new_storage_path:
            try:
                delete_product_image_file(
                    new_storage_path
                )
            except Exception:
                pass

        raise

    # Delete old file only AFTER the new
    # file and DB update succeeded.
    try:
        delete_product_image_file(
            old_storage_path
        )
    except HTTPException:
        # The new image is already valid.
        # Don't destroy the successful edit
        # because old-file cleanup failed.
        pass

    return updated_image