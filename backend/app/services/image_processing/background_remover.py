from functools import lru_cache
from io import BytesIO

from PIL import Image
from rembg import new_session, remove


MAX_PROCESSING_SIZE = (
    1600,
    1600,
)


@lru_cache(maxsize=1)
def get_rembg_session():
    return new_session(
        "u2netp"
    )


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

        input_image.thumbnail(
            MAX_PROCESSING_SIZE,
            Image.Resampling.LANCZOS,
        )

        session = get_rembg_session()

        result = remove(
            input_image,
            session=session,
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