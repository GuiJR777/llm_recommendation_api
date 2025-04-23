import json
import fakeredis
from unittest.mock import patch
from cache import redis_client as redis_module


# Objeto mock usado no teste, compatível com factory
class DummyObject:
    def __init__(self, value: str):
        self.value = value


class TestCacheResult:
    def test_if_should_store_and_retrieve_from_cache(self):
        # Arrange
        from cache.redis_client import cache_result

        fake_redis = fakeredis.FakeRedis()
        redis_module.redis_client = fake_redis
        redis_module.redis_available = True

        @cache_result(ttl=3600, factory=DummyObject)
        def recommend(user_id: str):
            return [DummyObject(f"generated-{user_id}")]

        user_id = "u-test"

        # Act
        result_1 = recommend(user_id)  # cache miss
        result_2 = recommend(user_id)  # cache hit

        # Assert
        assert isinstance(result_1[0], DummyObject)
        assert isinstance(result_2[0], DummyObject)
        assert result_1[0].value == "generated-u-test"
        assert result_2[0].value == "generated-u-test"

    def test_if_should_run_function_normally_when_redis_is_unavailable(self):
        # Arrange
        from redis.exceptions import ConnectionError
        from cache.redis_client import cache_result

        redis_module.redis_client = None
        redis_module.redis_available = False

        @cache_result(ttl=3600, factory=DummyObject)
        def recommend(user_id: str):
            return [DummyObject(f"safe-{user_id}")]

        # Act
        result = recommend("u-fallback")

        # Assert
        assert isinstance(result, list)
        assert isinstance(result[0], DummyObject)
        assert result[0].value == "safe-u-fallback"


class TestClearAllCache:
    def test_if_clear_all_cache_should_remove_all_keys(self):
        # Arrange
        from cache.redis_client import cache_result, clear_all_cache

        fake_redis = fakeredis.FakeRedis()
        redis_module.redis_client = fake_redis
        redis_module.redis_available = True

        @cache_result(ttl=3600, factory=DummyObject)
        def recommend(user_id: str):
            return [DummyObject(f"cache-{user_id}")]

        recommend("u1001")
        recommend("u2002")

        assert len(fake_redis.keys()) > 0

        # Act
        clear_all_cache()

        # Assert
        assert len(fake_redis.keys()) == 0


class TestMakeCacheKey:
    def test_if_should_generate_deterministic_hash_key_for_same_input(self):
        from cache.redis_client import make_cache_key

        key1 = make_cache_key(
            "recommend_for_user", user_id="u1001", strategy_name="history"
        )
        key2 = make_cache_key(
            "recommend_for_user", user_id="u1001", strategy_name="history"
        )

        assert isinstance(key1, str)
        assert key1 == key2
        assert len(key1) == 64  # SHA256

    def test_if_should_generate_different_key_for_different_inputs(self):
        from cache.redis_client import make_cache_key

        key1 = make_cache_key(
            "recommend_for_user", user_id="u1001", strategy_name="history"
        )
        key2 = make_cache_key(
            "recommend_for_user", user_id="u1001", strategy_name="preference"
        )
        key3 = make_cache_key(
            "recommend_for_user", user_id="u2002", strategy_name="history"
        )

        assert key1 != key2
        assert key1 != key3
        assert key2 != key3
