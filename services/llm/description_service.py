from services.llm.strategies.llm_chatgpt import LLMChatGPTStrategy
from services.llm.strategies.llm_emulator import LLMEmulatorStrategy
from services.llm.strategies.llm_strategy import LLMStrategy
from models.product import Product
from typing import Optional
from cache.redis_client import async_cache_result
from utils.logger import logger


class ProductDescriptionService:
    def __init__(self, strategy: LLMStrategy):
        self.strategy = strategy

    def set_strategy(self, llm: str):
        match llm:
            case "emulator":
                self.strategy = LLMEmulatorStrategy()
            case "chatgpt":
                self.strategy = LLMChatGPTStrategy()
            case _:
                raise NotImplementedError(f"LLM '{llm}' não implementado.")

    @async_cache_result(ttl=60 * 60 * 24)  # 24h
    async def describe(
        self, product: Product, user_id: Optional[str] = None
    ) -> str:
        try:
            return await self.strategy.generate_description(product, user_id)
        except Exception as e:
            logger.error(
                f"[{self.strategy.__class__.__name__}] Erro ao gerar descrição: {str(e)}"
            )
            # Fallback simples
            return f"O produto {product.name} é uma excelente escolha para quem busca {product.category.lower()}."
