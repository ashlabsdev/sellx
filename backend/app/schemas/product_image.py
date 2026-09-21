from datetime import datetime

from pydantic import BaseModel


class ProductImageResponse(BaseModel):
    id: int
    storage_path: str
    image_url: str
    display_order: int
    is_primary: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }