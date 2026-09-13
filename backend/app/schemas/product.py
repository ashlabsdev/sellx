from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    category_id: int | None = None
    description: str | None = None
    price: float
    condition: str
    location: str | None = None
    contact_phone: str | None = None


class ProductResponse(ProductCreate):
    id: int
    slug: str
    status: str

    model_config = {
        "from_attributes": True
    }