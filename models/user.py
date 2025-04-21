from typing import List, Dict


class User:
    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        age: int,
        gender: str,
        location: str,
        preferences: Dict,
        purchase_history: List[Dict],
        browsing_history: List[Dict],
        cart_events: List[Dict],
    ):
        self.id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.gender = gender
        self.location = location
        self.preferences = preferences
        self.purchase_history = purchase_history
        self.browsing_history = browsing_history
        self.cart_events = cart_events
