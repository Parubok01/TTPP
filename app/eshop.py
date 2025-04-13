from typing import Dict
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from services import ShippingService


class Product:
    def __init__(self, name: str, price: float, available_amount: int):
        self.name = name
        self.price = price
        self.available_amount = available_amount

    def is_available(self, requested_amount: int) -> bool:
        return self.available_amount >= requested_amount

    def buy(self, requested_amount: int):
        if not self.is_available(requested_amount):
            raise ValueError(f"Not enough {self.name} available")
        self.available_amount -= requested_amount

    def __eq__(self, other) -> bool:
        return isinstance(other, Product) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name


class ShoppingCart:
    def __init__(self):
        self.products: Dict[Product, int] = {}

    def contains_product(self, product: Product) -> bool:
        return product in self.products

    def calculate_total(self) -> float:
        return sum(product.price * count for product, count in self.products.items())

    def add_product(self, product: Product, amount: int):
        if not product.is_available(amount):
            raise ValueError(f"Product {product} has only {product.available_amount} items available")
        self.products[product] = self.products.get(product, 0) + amount

    def remove_product(self, product: Product):
        self.products.pop(product, None)

    def submit_cart_order(self) -> list[str]:
        product_ids = []
        for product, count in self.products.items():
            product.buy(count)
            product_ids.append(str(product))
        self.products.clear()
        return product_ids


@dataclass
class Order:
    cart: ShoppingCart
    shipping_service: ShippingService
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def place_order(self, shipping_type: str, due_date: datetime = None) -> str:
        if not self.cart.products:
            raise ValueError("Cannot place order with an empty cart")
        due_date = due_date or datetime.now(timezone.utc) + timedelta(seconds=3)
        product_ids = self.cart.submit_cart_order()
        return self.shipping_service.create_shipping(shipping_type, product_ids, self.order_id, due_date)


@dataclass
class Shipment:
    shipping_id: str
    shipping_service: ShippingService

    def check_shipping_status(self) -> str:
        return self.shipping_service.check_status(self.shipping_id)