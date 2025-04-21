from typing import List, Dict


class Product:
    def __init__(
        self,
        product_id: str,
        name: str,
        description: str,
        category: str,
        sub_category: str,
        price: float,
        brand: str,
        average_rating: float,
        num_reviews: int,
        stock: int,
        tags: List[str],
        image_url: str,
        specifications: Dict,
    ):
        self.id = product_id
        self.name = name
        self.description = description
        self.category = category
        self.sub_category = sub_category
        self.price = price
        self.brand = brand
        self.average_rating = average_rating
        self.num_reviews = num_reviews
        self.stock = stock
        self.tags = tags
        self.image_url = image_url
        self.specifications = specifications
