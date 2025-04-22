from utils.file_loader import load_json

BASE_DIR = "data"


def get_all_users():
    return load_json(f"{BASE_DIR}/users.json").get("users", [])


def get_user_by_id(user_id: str):
    users = get_all_users()
    return next((u for u in users if u["id"] == user_id), None)


def get_all_products():
    return load_json(f"{BASE_DIR}/products.json").get("products", [])


def get_product_by_id(product_id: str):
    products = get_all_products()
    return next((p for p in products if p["id"] == product_id), None)
