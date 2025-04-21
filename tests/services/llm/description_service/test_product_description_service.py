import pytest
import fakeredis
from cache import redis_client as redis_module
from services.llm.description_service import ProductDescriptionService
from services.llm.strategies.llm_strategy import LLMStrategy
from services.llm.strategies.llm_emulator import LLMEmulatorStrategy
from models.product import Product
from unittest.mock import AsyncMock


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
class TestDescribe:
    async def test_if_should_return_personalized_description(self):
        mock_strategy = AsyncMock(spec=LLMStrategy)
        mock_strategy.generate_description.return_value = "Personalizado!"

        service = ProductDescriptionService(mock_strategy)
        result = await service.describe(dummy_product, user_id="u1001")

        assert result == "Personalizado!"
        mock_strategy.generate_description.assert_awaited_once_with(
            dummy_product, "u1001"
        )

    async def test_if_should_return_generic_description_without_user(self):
        mock_strategy = AsyncMock(spec=LLMStrategy)
        mock_strategy.generate_description.return_value = "Genérico!"

        service = ProductDescriptionService(mock_strategy)
        result = await service.describe(dummy_product)

        assert result == "Genérico!"
        mock_strategy.generate_description.assert_awaited_once_with(
            dummy_product, None
        )

    async def test_if_should_return_cached_result_when_available(self):
        # Usa fakeredis no lugar do Redis real
        fake = fakeredis.FakeRedis()
        redis_module.redis_client = fake
        redis_module.redis_available = True

        service = ProductDescriptionService(LLMEmulatorStrategy())

        # Primeira chamada: gera e salva no cache
        first_result = await service.describe(dummy_product)

        # Segunda chamada: retorna do cache
        second_result = await service.describe(dummy_product)

        assert second_result == first_result
        assert isinstance(second_result, str)

    async def test_if_should_work_when_cache_is_disabled(self):
        from cache import redis_client as rc_module

        rc_module.redis_available = False

        mock_strategy = AsyncMock(spec=LLMStrategy)
        mock_strategy.generate_description.return_value = "Sem cache"

        service = ProductDescriptionService(mock_strategy)
        result = await service.describe(dummy_product)

        assert result == "Sem cache"


@pytest.mark.asyncio
class TestSetStrategy:
    async def test_if_should_use_new_strategy_after_set_strategy(self):
        strategy1 = AsyncMock(spec=LLMStrategy)
        strategy1.generate_description.return_value = "Primeira"

        strategy2 = AsyncMock(spec=LLMStrategy)
        strategy2.generate_description.return_value = "Segunda"

        service = ProductDescriptionService(strategy1)
        result1 = await service.describe(dummy_product)

        service.set_strategy(strategy2)
        result2 = await service.describe(dummy_product)

        assert result1 == "Primeira"
        assert result2 == "Segunda"
        strategy1.generate_description.assert_awaited_once()
        strategy2.generate_description.assert_awaited_once()
