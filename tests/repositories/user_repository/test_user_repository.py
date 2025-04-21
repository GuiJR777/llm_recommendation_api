from repositories.user_repository import UserRepository
from models.user import User


class TestUserRepository:
    def test_if_user_repository_should_return_user_by_id(self):
        # Arrange
        repo = UserRepository(path="data/users.json")

        # Act
        user = repo.get_by_id("u1001")

        # Assert
        assert isinstance(user, User)
        assert user.id == "u1001"

    def test_if_user_repository_should_return_user_dict(self):
        # Arrange
        repo = UserRepository(path="data/users.json")
        user = repo.get_by_id("u1001")

        # Act
        user_dict = repo.to_dict(user)

        # Assert
        assert isinstance(user_dict, dict)
        assert user_dict["id"] == "u1001"
