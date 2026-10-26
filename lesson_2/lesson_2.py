from abc import ABC, abstractmethod
from datetime import date
from enum import Enum, IntEnum

class MenuItem(ABC):
    def _init_(self, name:str, base_price: float):
        if base_price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.name = name
        self.base_price = base_price
    @property
    def name(self) -> str:
        return self._name
    @property
    def base_price(self) -> float:
        return self.base_price

    @abstractmethod
    def calculate_price(self) -> float:
        "Рассчитывает итоговую стоимость конкретного блюда."

    def __str__(self) -> str:
        return f"{self.name} — {self.calculate_price():.2f}"
       
class OrderStatus(IntEnum):
    NEW = 0
    COOKING = 1
    DELIVERING = 2
    DELIVERED = 3
    @property
    def title(self) -> str:
        return {
            OrderStatus.NEW: "Новый",
            OrderStatus.COOKING: "Готовится",
            OrderStatus.DELIVERING: "В доставке",
            OrderStatus.DELIVERED: "Доставлен",
            }[self]
class Order:
    def __init__(self):
        self.__items: list[MenuItem] = []          
        self.__status = OrderStatus.NEW            
 
    @property
    def status(self) -> OrderStatus:
        
        return self.__status
 
    @property
    def items(self) -> tuple[MenuItem, ...]:
        return tuple(self.__items)                 
 
    def next_step(self) -> None:
        if self.__status == OrderStatus.DELIVERED:
            raise RuntimeError("Заказ уже доставлен, дальше двигаться некуда")
        self.__status = OrderStatus(self.__status + 1)
        print(f"Статус заказа: {self.__status.title}")
 
    def add_item(self, item: MenuItem) -> None:
        if self.__status >= OrderStatus.COOKING:
            raise RuntimeError(
                f"Нельзя добавить блюдо: заказ уже в статусе «{self.__status.title}»"
            )
        self.__items.append(item)
 
    def get_total_cost(self) -> float:
        return sum(i.calculate_price() for i in self.__items)
 
    def pay(self, payment_method: PaymentStrategy) -> None:
        if not self.__items:
            raise RuntimeError("Корзина пуста — оплачивать нечего")
        payment_method.collect_payment(self.get_total_cost())

class PaymentStrategy(ABC):
    @abstractmethod
    def collect_payment(self, amount: float) -> None:
        ...

class PizzaSize(Enum):
    SMALL = "маленькая"
    MEDIUM = "средняя"
    LARGE = "большая"
 
 
class Pizza(MenuItem):
    def __init__(self, name: str, base_price: float, size: PizzaSize):
        super().__init__(name, base_price)
        self._size = size
 
    def calculate_price(self) -> float:
        if self._size == PizzaSize.LARGE:
            return self.base_price * 1.30
        return self.base_price
 
    @property
    def name(self) -> str:
        return f"{self._name} ({self._size.value})"
 
 
class Drink(MenuItem):
    def __init__(self, name: str, base_price: float, is_ice: bool):
        super().__init__(name, base_price)
        self._is_ice = is_ice
 
    def calculate_price(self) -> float:
        return self.base_price  # лёд на цену не влияет
 
    @property
    def name(self) -> str:
        return f"{self._name} со льдом" if self._is_ice else self._name
 
 
class ComboSet(MenuItem):
    DISCOUNT = 0.15
 
    def __init__(self, name: str, items: list[MenuItem]):
        super().__init__(name, 0)
        self._items = list(items)  # защитная копия
 
    def calculate_price(self) -> float:
        return sum(i.calculate_price() for i in self._items) * (1 - self.DISCOUNT)
 
    @property
    def name(self) -> str:
        inner = ", ".join(i.name for i in self._items)
        return f"{self._name} [{inner}]"
 
class CardPayment(PaymentStrategy):
    def __init__(self, card_number: str, expiry_month: int, expiry_year: int):
        self._card_number = card_number
        self._expiry = (expiry_year, expiry_month)
 
    def collect_payment(self, amount: float) -> None:
        today = date.today()
        if self._expiry < (today.year, today.month):
            raise ValueError(
                f"Срок действия карты истёк: {self._expiry[1]:02d}/{self._expiry[0]}"
            )
        print(f"С карты **** {self._card_number[-4:]} списано {amount:.2f}")
 
 
class CashPayment(PaymentStrategy):
    def collect_payment(self, amount: float) -> None:
        print(f"Оплата наличными курьеру: приготовьте {amount:.2f}")

