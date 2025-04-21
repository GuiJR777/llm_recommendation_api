from typing import Dict


class Product:
    def __init__(
        self,
        product_id: str,
        name: str,
        category: str,
        brand: str,
        description: str,
        price: float,
        specifications: Dict,
    ):
        self.id = product_id
        self.name = name
        self.category = category
        self.brand = brand
        self.description = description
        self.price = price
        self.specifications = specifications
