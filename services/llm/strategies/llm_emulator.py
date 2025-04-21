from services.llm.strategies.llm_strategy import LLMStrategy
from models.product import Product
from mock.llm_api_mock import LLMApiMock
from typing import Optional


class LLMEmulatorStrategy(LLMStrategy):
    def __init__(self):
        self.llm = LLMApiMock()

    async def generate_description(
        self, product: Product, user_id: Optional[str] = None
    ) -> str:
        try:
            if user_id:
                return await self.llm.generate_response(
                    {
                        "type": "personalized_description",
                        "user_id": user_id,
                        "product_id": product.id,
                    }
                )
            else:
                return await self.llm.generate_response(
                    {"type": "generic_description", "product_id": product.id}
                )
        except Exception:
            return "Não foi possível gerar uma descrição para este produto no momento."
