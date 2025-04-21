class Recommendation:
    def __init__(self, product_id: str, score: float, reason: str):
        self.product_id = product_id
        self.score = score
        self.reason = reason
