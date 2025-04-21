import json
from models.user import User

class UserRepository:
    def __init__(self, path='data/users.json'):
        with open(path, encoding='utf-8') as f:
            self.users = json.load(f)['users']

    def get_by_id(self, user_id: str) -> User:
        data = next((u for u in self.users if u['id'] == user_id), None)
        if not data:
            raise ValueError("User not found")
        data["user_id"] = data.pop("id")
        return User(**data)

    def to_dict(self, user: User):
        return user.__dict__
