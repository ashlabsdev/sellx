from fastapi import APIRouter

from app.api.routes import categories
from app.api.routes import health
from app.api.routes import product_images
from app.api.routes import products


api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(product_images.router)