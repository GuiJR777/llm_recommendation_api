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
        match strategy_name:
            case "preference":
                self.strategy = PreferenceBasedRecommendationStrategy()
            case "history":
                self.strategy = HistoryBasedRecommendationStrategy()
            case _:
                logger.warning(
                    f"[Recommendation Warning] Estratégia '{strategy_name}' não reconhecida. Usando padrão: history"  # noqa
                )
                self.strategy = HistoryBasedRecommendationStrategy()

        logger.info(
            f"[Recommendation Strategy] Estratégia definida: {self.strategy.__class__.__name__}"  # noqa
        )

    @cache_result(factory=Recommendation)
    def recommend_for_user(
        self, user_id: str, strategy_name: str = "history"
    ) -> list[Recommendation]:
        logger.info(
            f"[Recommendation Start] user_id={user_id}, strategy={strategy_name}"  # noqa
        )

        try:
            self.set_strategy(strategy_name)
            recommendations = self.strategy.recommend(user_id)
            logger.info(
                f"[Recommendation Success] user_id={user_id}, total={len(recommendations)} recommendation(s)."  # noqa
            )
            return recommendations

        except ValueError as ve:
            logger.error(
                f"[Recommendation Error] user_id={user_id}, strategy={strategy_name} | {str(ve)}"  # noqa
            )
            raise ValueError(
                f"Erro ao processar recomendações para o usuário {user_id}: {str(ve)}"  # noqa
            )

        except Exception as e:
            logger.exception(
                f"[Recommendation Error] user_id={user_id}, strategy={strategy_name} | {str(e)}"  # noqa
            )
            return []
