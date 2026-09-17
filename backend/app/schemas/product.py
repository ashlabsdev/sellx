from pydantic import BaseModel

from app.schemas.category import CategorySummary


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

    model_config = {
        "from_attributes": True
    }