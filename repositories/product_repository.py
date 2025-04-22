import json
from models.product import Product


class ProductRepository:
    def __init__(self, path="web_interface/backend/data/products.json"):
        with open(path, encoding="utf-8") as f:
            self.products = json.load(f)["products"]

            for product in self.products:
                product["product_id"] = product["id"]
                del product["id"]

    def get_by_id(self, product_id: str) -> Product:
        data = next(
            (p for p in self.products if p["product_id"] == product_id), None
        )
        if not data:
            raise ValueError("Product not found")

        return Product(**data)

    def to_dict(self, product: Product):
        return product.__dict__
