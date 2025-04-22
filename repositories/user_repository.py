import json
from models.user import User


class UserRepository:
    def __init__(self, path="web_interface/backend/data/users.json"):
        with open(path, encoding="utf-8") as f:
            self.users = json.load(f)["users"]

            for user in self.users:
                user["user_id"] = user["id"]
                del user["id"]

    def get_by_id(self, user_id: str) -> User:
        data = next((u for u in self.users if u["user_id"] == user_id), None)
        if not data:
            raise ValueError("User not found")

        return User(**data)

    def to_dict(self, user: User):
        return user.__dict__
