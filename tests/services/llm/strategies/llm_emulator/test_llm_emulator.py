import pytest
from services.llm.strategies.llm_emulator import LLMEmulatorStrategy
from models.product import Product
from unittest.mock import patch

# Produto mínimo necessário para teste
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

fake_product = Product(
    product_id="invalid",
    name="Produto Desconhecido",
    category="desconhecido",
    sub_category="outros",
    brand="N/A",
    description="Descrição inexistente",
    price=0.0,
    average_rating=0.0,
    num_reviews=0,
    stock=0,
    tags=[],
    image_url="placeholder.jpg",
    specifications={},
)


class TestLLMEmulatorStrategyGenerateDescription:
    @pytest.mark.asyncio
    async def test_if_should_return_personalized_description_with_user(self):
        strategy = LLMEmulatorStrategy()
        result = await strategy.generate_description(
            dummy_product, user_id="u1001"
        )
        assert isinstance(result, str)
        assert dummy_product.name in result

    @pytest.mark.asyncio
    async def test_if_should_return_generic_description_without_user(self):
        strategy = LLMEmulatorStrategy()
        result = await strategy.generate_description(dummy_product)
        assert isinstance(result, str)
        assert dummy_product.name in result

    @pytest.mark.asyncio
    async def test_if_should_handle_nonexistent_product_gracefully(self):
        strategy = LLMEmulatorStrategy()
        result = await strategy.generate_description(fake_product)
        assert isinstance(result, str)
        assert "não disponível" in result.lower()

    @pytest.mark.asyncio
    async def test_if_should_fallback_to_generic_when_user_not_found(self):
        strategy = LLMEmulatorStrategy()
        result = await strategy.generate_description(
            dummy_product, user_id="usuario_invalido"
        )
        assert isinstance(result, str)
        assert dummy_product.name in result

    @pytest.mark.asyncio
    async def test_if_should_return_fallback_on_llm_error(self):
        strategy = LLMEmulatorStrategy()

        with patch(
            "mock.llm_api_mock.LLMApiMock.generate_response",
            side_effect=Exception("Erro simulado"),
        ):
            result = await strategy.generate_description(
                dummy_product, user_id="u1001"
            )

        assert isinstance(result, str)
        assert (
            "não foi possível gerar uma descrição para este produto no momento."
            in result.lower()
        )
