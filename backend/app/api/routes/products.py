from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import (
    add_product,
    get_product_by_id,
    list_products,
)

router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


@router.get("", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db),
):
    return list_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.post(
    "",
    response_model=ProductResponse,
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
):
    return add_product(db, data)