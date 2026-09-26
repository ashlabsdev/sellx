from io import BytesIO

from PIL import Image


MAX_IMAGE_SIZE = 1600


def resize_image(
    image: Image.Image,
) -> Image.Image:
    result = image.copy()

    result.thumbnail(
        (
            MAX_IMAGE_SIZE,
            MAX_IMAGE_SIZE,
        ),
        Image.Resampling.LANCZOS,
    )

    return result


def convert_to_webp(
    image: Image.Image,
    quality: int = 85,
) -> bytes:
    image = resize_image(
        image
    )

    if image.mode not in (
        "RGB",
        "RGBA",
    ):
        image = image.convert(
            "RGB"
        )

    output = BytesIO()

    image.save(
        output,
        format="WEBP",
        quality=quality,
        method=6,
    )

    return output.getvalue()

def convert_to_png(
    image: Image.Image,
) -> bytes:
    image = resize_image(
        image
    )

    if image.mode != "RGBA":
        image = image.convert(
            "RGBA"
        )

    output = BytesIO()

    image.save(
        output,
        format="PNG",
        optimize=True,
    )

    return output.getvalue()