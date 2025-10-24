from typing import Dict, List, Optional
from threading import RLock


class InMemoryDB:
    """
    A simple thread-safe in-memory persistence layer for products.
    Designed to be swappable for a database later with minimal changes.
    """
    def __init__(self) -> None:
        self._items: Dict[int, Dict] = {}
        self._lock = RLock()

    def list_all(self) -> List[Dict]:
        with self._lock:
            return list(self._items.values())

    def get(self, product_id: int) -> Optional[Dict]:
        with self._lock:
            return self._items.get(product_id)

    def create(self, product: Dict) -> None:
        with self._lock:
            self._items[product["id"]] = product

    def update(self, product_id: int, product: Dict) -> None:
        with self._lock:
            self._items[product_id] = product

    def delete(self, product_id: int) -> None:
        with self._lock:
            if product_id in self._items:
                del self._items[product_id]


# Singleton in-memory DB instance for the app lifecycle
db = InMemoryDB()
