from fastapi import APIRouter, HTTPException
from services.data_service import (
    get_all_users,
    get_user_by_id,
    get_all_products,
    get_product_by_id,
)

router = APIRouter(prefix="/api")


@router.get("/users")
def read_all_users():
    return get_all_users()


@router.get("/users/{user_id}")
def read_user(user_id: str):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/products")
def read_all_products():
    return get_all_products()


@router.get("/products/{product_id}")
def read_product(product_id: str):
    product = get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
