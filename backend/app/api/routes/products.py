from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_admin
from app.models.admin import Admin

from app.core.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import (
    add_product,
    edit_product,
    get_product_by_id,
    list_products,
    remove_product,
)


router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)

@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_products(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=12,
        ge=1,
        le=100,
    ),
    search: str | None = None,
    category_id: int | None = None,
    status: str | None = "active",
    db: Session = Depends(get_db),
):
    return list_products(
        db,
        search=search,
        category_id=category_id,
        status=status,
        page=page,
        page_size=page_size,
    )

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
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    return add_product(db, data)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return edit_product(db, product, data)


@router.delete(
    "/{product_id}",
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    remove_product(db, product)

    return {
        "message": "Product deleted successfully",
    }