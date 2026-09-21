from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_admin
from app.models.admin import Admin

from app.core.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import (
    add_category,
    edit_category,
    get_category_by_id,
    list_categories,
    remove_category,
)


router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"],
)


@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories(
    db: Session = Depends(get_db),
):
    return list_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = get_category_by_id(
        db,
        category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.post(
    "",
    response_model=CategoryResponse,
)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    return add_category(
        db,
        data,
    )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    category = get_category_by_id(
        db,
        category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return edit_category(
        db,
        category,
        data,
    )


@router.delete(
    "/{category_id}",
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    category = get_category_by_id(
        db,
        category_id,
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    remove_category(
        db,
        category,
    )

    return {
        "message": "Category deleted successfully",
    }