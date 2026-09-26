from typing import Literal

from pydantic import BaseModel


BackgroundColor = Literal[
    "white",
    "grey",
    "black",
]


class ImageProcessRequest(BaseModel):
    background: BackgroundColor


class ImageProcessResponse(BaseModel):
    image_base64: str
    content_type: str


class ImageSaveRequest(BaseModel):
    background: BackgroundColor