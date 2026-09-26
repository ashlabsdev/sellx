from io import BytesIO

from PIL import Image
from rembg import remove


def remove_image_background(
    image_bytes: bytes,
) -> Image.Image:
    if not image_bytes:
        raise ValueError(
            "Image data is empty"
        )

    try:
        input_image = Image.open(
            BytesIO(image_bytes)
        )

        input_image.load()

        result = remove(
            input_image
        )

        if not isinstance(
            result,
            Image.Image,
        ):
            raise ValueError(
                "Background removal returned "
                "an invalid image"
            )

        return result.convert("RGBA")

    except Exception as exc:
        raise ValueError(
            "Failed to remove image background"
        ) from exc