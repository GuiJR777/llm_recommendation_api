from services.recommendation_service.strategies.base_strategy import (
    RecommendationStrategy,
)
from services.recommendation_service.strategies.history_strategy import (
    HistoryBasedRecommendationStrategy,
)
from services.recommendation_service.strategies.preference_strategy import (
    PreferenceBasedRecommendationStrategy,
)


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

    def recommend_for_user(self, user_id: str, strategy_name: str = "history"):
        self.set_strategy(strategy_name)
        return self.strategy.recommend(user_id)
