import pytest
from services.llm.strategies.llm_chatgpt import LLMChatGPTStrategy
from models.product import Product
from unittest.mock import AsyncMock, patch


dummy_product = Product(
    product_id="p1005",
    name="Fones de Ouvido Bluetooth TechMaster Pro",
    category="áudio",
    sub_category="fones",
    brand="TechMaster",
    description="Som imersivo com cancelamento de ruído",
    price=199.90,
    average_rating=4.5,
    num_reviews=120,
    stock=50,
    tags=["áudio", "tecnologia"],
    image_url="techmaster_pro.jpg",
    specifications={"bateria": "20h", "conectividade": "Bluetooth 5.0"},
)


@pytest.mark.asyncio
class TestLLMChatGPTStrategy:
    async def test_if_should_return_description_with_user(self):
        strategy = LLMChatGPTStrategy()

        with patch.object(
            strategy.client.chat.completions,
            "create",
            new=AsyncMock(
                return_value=AsyncMock(
                    choices=[
                        AsyncMock(
                            message=AsyncMock(content="Resposta com usuário")
                        )
                    ]
                )
            ),
        ):
            result = await strategy.generate_description(
                dummy_product, user_id="u1003"
            )

        assert result == "Resposta com usuário"

    async def test_if_should_return_description_without_user(self):
        strategy = LLMChatGPTStrategy()

        with patch.object(
            strategy.client.chat.completions,
            "create",
            new=AsyncMock(
                return_value=AsyncMock(
                    choices=[
                        AsyncMock(
                            message=AsyncMock(content="Resposta genérica")
                        )
                    ]
                )
            ),
        ):
            result = await strategy.generate_description(dummy_product)

        assert result == "Resposta genérica"

    async def test_if_should_return_fallback_on_exception(self):
        strategy = LLMChatGPTStrategy()

        with patch.object(
            strategy.client.chat.completions,
            "create",
            side_effect=Exception("Erro simulado"),
        ):
            result = await strategy.generate_description(
                dummy_product, user_id="u1001"
            )

        assert isinstance(result, str)
        assert dummy_product.name.lower() in result.lower()
        assert dummy_product.category.lower() in result.lower()
