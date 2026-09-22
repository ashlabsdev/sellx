from datetime import datetime

from pydantic import BaseModel


class ProductImageUpdate(BaseModel):
    display_order: int | None = None
    is_primary: bool | None = None

class ProductImageReorder(BaseModel):
    image_ids: list[int]

class ProductImageResponse(BaseModel):
    id: int
    storage_path: str
    image_url: str
    display_order: int | None = None
    is_primary: bool | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }