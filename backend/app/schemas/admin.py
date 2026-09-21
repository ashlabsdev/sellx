from pydantic import BaseModel, ConfigDict


class AdminResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )