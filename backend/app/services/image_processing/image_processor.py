from io import BytesIO

from PIL import Image, ImageOps

from app.services.image_processing.background_composer import (
    apply_background,
)

from app.services.image_processing.background_remover import (
    remove_image_background,
)

from app.services.image_processing.image_optimizer import (
    convert_to_png,
    convert_to_webp,
)


ALLOWED_BACKGROUNDS = {
    "white",
    "grey",
    "black",
}


def apply_image_transformations(
    image: Image.Image,
    rotation: int = 0,
    crop: dict | None = None,
) -> Image.Image:

    # Correct phone-camera EXIF orientation first.
    image = ImageOps.exif_transpose(
        image
    )

    # Our API treats positive rotation as clockwise.
    if rotation:
        image = image.rotate(
            -rotation,
            expand=True,
        )

    if crop:
        x = crop["x"]
        y = crop["y"]

        width = crop["width"]
        height = crop["height"]

        right = x + width
        bottom = y + height

        if (
            x < 0
            or y < 0
            or width <= 0
            or height <= 0
        ):
            raise ValueError(
                "Invalid crop dimensions"
            )

        if (
            right > image.width
            or bottom > image.height
        ):
            raise ValueError(
                "Crop area exceeds image bounds"
            )

        image = image.crop(
            (
                x,
                y,
                right,
                bottom,
            )
        )

    return image


def image_to_png_bytes(
    image: Image.Image,
) -> bytes:
    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG",
    )

    return buffer.getvalue()


def create_transparent_preview(
    image_bytes: bytes,
) -> bytes:
    transparent_image = (
        remove_image_background(
            image_bytes
        )
    )

    return convert_to_png(
        transparent_image
    )


def process_product_image(
    image_bytes: bytes,
    background: str,
    rotation: int = 0,
    crop: dict | None = None,
) -> bytes:

    if background not in ALLOWED_BACKGROUNDS:
        raise ValueError(
            "Invalid background color"
        )

    # 1. Decode original JPG / PNG / WebP.
    try:
        with Image.open(
            BytesIO(image_bytes)
        ) as source_image:

            # Make an independent in-memory image
            # before Image.open() closes.
            image = source_image.copy()

    except Exception as exc:
        raise ValueError(
            "Unable to read image"
        ) from exc

    # 2. EXIF orientation -> rotate -> crop.
    image = apply_image_transformations(
        image,
        rotation=rotation,
        crop=crop,
    )

    # 3. Convert transformed Pillow image
    # back into bytes for rembg.
    transformed_bytes = (
        image_to_png_bytes(
            image
        )
    )

    # 4. Remove background from the
    # already transformed image.
    transparent_image = (
        remove_image_background(
            transformed_bytes
        )
    )

    # 5. Apply selected SellX background.
    final_image = apply_background(
        transparent_image,
        background,
    )

    # 6. Final saved marketplace image
    # is always WebP.
    return convert_to_webp(
        final_image
    )