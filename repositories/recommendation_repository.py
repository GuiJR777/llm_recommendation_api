import json
from models.recommendation import Recommendation

class RecommendationRepository:
    def __init__(self, path='data/recommendations_examples.json'):
        with open(path, encoding='utf-8') as f:
            self.data = json.load(f)

    def get_user_recommendations(self, user_id: str):
        user_data = next((u for u in self.data['user_recommendations'] if u['user_id'] == user_id), None)
        if not user_data:
            raise ValueError("Recommendations not found for user")
        return [Recommendation(**r) for r in user_data['recommendations']]

    def to_dict(self, recommendation: Recommendation):
        return recommendation.__dict__
