from pydantic import BaseModel, Field

from app.schemas.category import CategorySummary
from app.schemas.product_image import ProductImageResponse

class ProductCreate(BaseModel):
    name: str
    category_id: int | None = None
    description: str | None = None
    price: float
    condition: str
    location: str | None = None
    contact_phone: str | None = None


class ProductUpdate(BaseModel):
    name: str
    category_id: int | None = None
    description: str | None = None
    price: float
    condition: str
    location: str | None = None
    contact_phone: str | None = None
    status: str


class ProductResponse(ProductCreate):
    id: int
    slug: str
    status: str
    category: CategorySummary | None = None
    images: list[ProductImageResponse] = Field(
        default_factory=list
    )

    model_config = {
        "from_attributes": True
    }