from services.llm.strategies.llm_strategy import LLMStrategy
from models.product import Product
from typing import Optional
from cache.redis_client import async_cache_result


class ProductDescriptionService:
    def __init__(self, strategy: LLMStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: LLMStrategy):
        self.strategy = strategy

    @async_cache_result(ttl=60 * 60 * 24)  # 24h
    async def describe(
        self, product: Product, user_id: Optional[str] = None
    ) -> str:
        return await self.strategy.generate_description(product, user_id)
