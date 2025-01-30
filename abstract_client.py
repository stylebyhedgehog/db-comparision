from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DatabaseClientInterface(ABC):
    """
    Интерфейс для работы с различными базами данных.
    """

    @abstractmethod
    def create_user(self, name: str, email: str, registration_date: str) -> Any:
        """Создать нового пользователя."""
        pass

    @abstractmethod
    def read_user(self, user_id: int) -> Dict[str, Any]:
        """Получить информацию о пользователе по его ID."""
        pass

    @abstractmethod
    def update_user(self, user_id: int, data: Dict[str, Any]) -> None:
        """Обновить информацию о пользователе."""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """Удалить пользователя по его ID."""
        pass

    @abstractmethod
    def create_product(self, name: str, price: float, category_id: int) -> Any:
        """Создать новый товар."""
        pass

    @abstractmethod
    def read_product(self, product_id: int) -> Dict[str, Any]:
        """Получить информацию о товаре по его ID."""
        pass

    @abstractmethod
    def update_product(self, product_id: int, data: Dict[str, Any]) -> None:
        """Обновить информацию о товаре."""
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        """Удалить товар по его ID."""
        pass

    @abstractmethod
    def create_category(self, category_name: str) -> Any:
        """Создать новую категорию."""
        pass

    @abstractmethod
    def read_category(self, category_id: int) -> Dict[str, Any]:
        """Получить информацию о категории по её ID."""
        pass

    @abstractmethod
    def update_category(self, category_id: int, data: Dict[str, Any]) -> None:
        """Обновить информацию о категории."""
        pass

    @abstractmethod
    def delete_category(self, category_id: int) -> None:
        """Удалить категорию по её ID."""
        pass

    @abstractmethod
    def create_order(self, user_id: int, order_date: str, total: float) -> Any:
        """Создать новый заказ."""
        pass

    @abstractmethod
    def read_order(self, order_id: int) -> Dict[str, Any]:
        """Получить информацию о заказе по его ID."""
        pass

    @abstractmethod
    def update_order(self, order_id: int, data: Dict[str, Any]) -> None:
        """Обновить информацию о заказе."""
        pass

    @abstractmethod
    def delete_order(self, order_id: int) -> None:
        """Удалить заказ по его ID."""
        pass

    @abstractmethod
    def create_order_item(self, order_id: int, product_id: int, quantity: int) -> None:
        """Добавить товар в заказ."""
        pass

    @abstractmethod
    def read_order_items(self, order_id: int) -> List[Dict[str, Any]]:
        """Получить список товаров в заказе."""
        pass

    @abstractmethod
    def get_orders_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Получить все заказы пользователя по его ID."""
        pass

    @abstractmethod
    def get_products_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Получить все товары, купленные пользователем по его ID."""
        pass

    @abstractmethod
    def get_products_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        """Получить товары по ID категории."""
        pass
