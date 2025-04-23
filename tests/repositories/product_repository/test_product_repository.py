from repositories.product_repository import ProductRepository
from models.product import Product


class TestProductRepository:
    def test_if_product_repository_should_return_product_by_id(self):
        # Arrange
        repo = ProductRepository(path="web_interface/backend/data/products.json")

        # Act
        product = repo.get_by_id("p1005")

        # Assert
        assert isinstance(product, Product)
        assert product.id == "p1005"

    def test_if_product_repository_should_return_product_dict(self):
        # Arrange
        repo = ProductRepository(path="web_interface/backend/data/products.json")
        product = repo.get_by_id("p1005")

        # Act
        product_dict = repo.to_dict(product)

        # Assert
        assert isinstance(product_dict, dict)
        assert product_dict["id"] == "p1005"
