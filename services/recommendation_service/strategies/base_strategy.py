from abc import ABC, abstractmethod
from models.recommendation import Recommendation


class RecommendationStrategy(ABC):
    @abstractmethod
    def recommend(self, user_id: str) -> list[Recommendation]:
        pass
