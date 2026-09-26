from PIL import Image


BACKGROUND_COLORS = {
    "white": (
        255,
        255,
        255,
        255,
    ),
    "grey": (
        220,
        220,
        220,
        255,
    ),
    "black": (
        0,
        0,
        0,
        255,
    ),
}


def apply_background(
    image: Image.Image,
    background: str,
) -> Image.Image:
    if background not in BACKGROUND_COLORS:
        raise ValueError(
            "Background must be "
            "white, grey, or black"
        )

    foreground = image.convert(
        "RGBA"
    )

    canvas = Image.new(
        "RGBA",
        foreground.size,
        BACKGROUND_COLORS[
            background
        ],
    )

    canvas.alpha_composite(
        foreground
    )

    return canvas.convert("RGB")