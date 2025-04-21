from services.recommendation_service.strategies.base_strategy import (
    RecommendationStrategy,
)
from services.recommendation_service.strategies.history_strategy import (
    HistoryBasedRecommendationStrategy,
)
from services.recommendation_service.strategies.preference_strategy import (
    PreferenceBasedRecommendationStrategy,
)
from cache.redis_client import cache_result
from models.recommendation import Recommendation
from utils.logger import logger


class RecommendationService:
    def __init__(self):
        self.strategy = HistoryBasedRecommendationStrategy()

    def set_strategy(self, strategy_name: str):
        strategies: dict[str, RecommendationStrategy] = {
            "history": HistoryBasedRecommendationStrategy(),
            "preference": PreferenceBasedRecommendationStrategy(),
        }
        self.strategy = strategies.get(
            strategy_name, HistoryBasedRecommendationStrategy()
        )
        logger.info(f"Estratégia definida: {self.strategy.__class__.__name__}")

    @cache_result(factory=Recommendation)
    def recommend_for_user(
        self, user_id: str, strategy_name: str = "history"
    ) -> list[Recommendation]:
        logger.info(
            f"Gerando recomendações para usuário '{user_id}' com estratégia '{strategy_name}'"  # noqa
        )
        self.set_strategy(strategy_name)
        return self.strategy.recommend(user_id)
