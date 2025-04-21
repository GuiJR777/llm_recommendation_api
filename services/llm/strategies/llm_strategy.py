from abc import ABC, abstractmethod
from models.product import Product
from typing import Optional


class LLMStrategy(ABC):
    @abstractmethod
    async def generate_description(
        self, product: Product, user_id: Optional[str] = None
    ) -> str:
        pass
