from pathlib import Path

from app.services.image_processing.image_processor import (
    process_product_image,
)

image_bytes = Path(
    "test_product.jpeg"
).read_bytes()

result = process_product_image(
    image_bytes,
    "white",
)

Path(
    "test_product_white.webp"
).write_bytes(
    result
)