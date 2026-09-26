from PIL import Image

from app.services.image_processing.background_composer import (
    apply_background,
)

from app.services.image_processing.background_remover import (
    remove_image_background,
)

from app.services.image_processing.image_optimizer import (
    convert_to_webp,
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
) -> bytes:
    if background not in ALLOWED_BACKGROUNDS:
        raise ValueError(
            "Invalid background color"
        )

    transparent_image: Image.Image = (
        remove_image_background(
            image_bytes
        )
    )

    final_image = apply_background(
        transparent_image,
        background,
    )

    return convert_to_webp(
        final_image
    )