from typing import List, Optional
from ..models.product import db


class ProductRepository:
    """
    Repository layer providing CRUD operations for products.
    Backed by an in-memory DB, designed to be easily swapped with real persistence.
    """

    # PUBLIC_INTERFACE
    def list_products(self) -> List[dict]:
        """Return all products as list of dicts."""
        return db.list_all()

    # PUBLIC_INTERFACE
    def get_product(self, product_id: int) -> Optional[dict]:
        """Return a product by id or None if not found."""
        return db.get(product_id)

    # PUBLIC_INTERFACE
    def create_product(self, product: dict) -> None:
        """Create a new product. Assumes id uniqueness has been pre-validated."""
        db.create(product)

    # PUBLIC_INTERFACE
    def update_product(self, product_id: int, product: dict) -> None:
        """Replace an existing product by id."""
        db.update(product_id, product)

    # PUBLIC_INTERFACE
    def delete_product(self, product_id: int) -> None:
        """Delete a product by id (no-op if not found)."""
        db.delete(product_id)

    # PUBLIC_INTERFACE
    def exists(self, product_id: int) -> bool:
        """Check if a product exists by id."""
        return db.get(product_id) is not None


# Singleton repository
product_repository = ProductRepository()
