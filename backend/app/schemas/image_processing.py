from typing import Literal

from pydantic import BaseModel, Field


BackgroundColor = Literal[
    "white",
    "grey",
    "black",
]


class CropData(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)

    width: int = Field(gt=0)
    height: int = Field(gt=0)


class ImageEditRequest(BaseModel):
    background: BackgroundColor

    rotation: Literal[
        0,
        90,
        180,
        270,
    ] = 0

    crop: CropData | None = None


class ImageProcessResponse(BaseModel):
    image_base64: str
    content_type: str


class ImageSaveRequest(ImageEditRequest):
    pass