from services.llm.strategies.llm_strategy import LLMStrategy
from models.product import Product
from mock.llm_api_mock import LLMApiMock
from typing import Optional
from utils.logger import logger


class LLMEmulatorStrategy(LLMStrategy):
    def __init__(self):
        self.llm = LLMApiMock()

    async def generate_description(
        self, product: Product, user_id: Optional[str] = None
    ) -> str:
        product_id = product.id

        payload = {
            "type": (
                "personalized_description"
                if user_id
                else "generic_description"
            ),
            "product_id": product_id,
            "user_id": user_id,
        }

        logger.info(f"[LLM Request] {payload}")

        try:
            response = await self.llm.generate_response(payload)
            logger.info(
                f"[LLM Response] product_id={product_id}, user_id={user_id}, response={response}"  # noqa
            )
            return response

        except Exception as e:
            logger.exception(
                f"[LLM Error] Failed to generate description | payload: {payload}, error: {e}"  # noqa
            )
            return self._fallback_description(product)

    def _fallback_description(self, product: Product) -> str:
        return (
            f"{product.name} é um produto da categoria {product.category} que oferece "  # noqa
            f"{product.description}. Ideal para quem busca qualidade e praticidade."  # noqa
        )
