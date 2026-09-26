import uuid

from fastapi import HTTPException, UploadFile

from app.core.config import SUPABASE_STORAGE_BUCKET
from app.core.supabase import supabase


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


async def upload_product_image(
    product_id: int,
    file: UploadFile,
) -> tuple[str, str]:

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, PNG, and WebP images are allowed",
        )

    extension = ALLOWED_IMAGE_TYPES[
        file.content_type
    ]

    filename = (
        f"{uuid.uuid4()}{extension}"
    )

    storage_path = (
        f"products/{product_id}/{filename}"
    )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty",
        )

    try:
        supabase.storage.from_(
            SUPABASE_STORAGE_BUCKET
        ).upload(
            path=storage_path,
            file=file_bytes,
            file_options={
                "content-type": file.content_type,
            },
        )

        image_url = (
            supabase.storage.from_(
                SUPABASE_STORAGE_BUCKET
            ).get_public_url(
                storage_path
            )
        )

        return storage_path, image_url

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to upload image",
        ) from exc

def delete_product_image_file(
    storage_path: str,
) -> None:
    try:
        supabase.storage.from_(
            SUPABASE_STORAGE_BUCKET
        ).remove(
            [storage_path]
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete image from storage",
        ) from exc

# 18.11 - Download an existing image from Supabase
def download_product_image_file(
    storage_path: str,
) -> bytes:
    try:
        file_bytes = (
            supabase.storage.from_(
                SUPABASE_STORAGE_BUCKET
            ).download(
                storage_path
            )
        )

        if not file_bytes:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Product image file "
                    "was not found"
                ),
            )

        return file_bytes

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to download image "
                "from storage"
            ),
        ) from exc

# 18.12 — Upload processed WebP
def upload_processed_product_image(
    product_id: int,
    image_bytes: bytes,
) -> tuple[str, str]:
    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="Processed image is empty",
        )

    filename = (
        f"{uuid.uuid4()}.webp"
    )

    storage_path = (
        f"products/{product_id}/"
        f"{filename}"
    )

    try:
        supabase.storage.from_(
            SUPABASE_STORAGE_BUCKET
        ).upload(
            path=storage_path,
            file=image_bytes,
            file_options={
                "content-type":
                    "image/webp",
            },
        )

        image_url = (
            supabase.storage.from_(
                SUPABASE_STORAGE_BUCKET
            ).get_public_url(
                storage_path
            )
        )

        return (
            storage_path,
            image_url,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to upload "
                "processed image"
            ),
        ) from exc