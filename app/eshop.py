"""E-shop module containing Product, ShoppingCart, Order, and Shipment classes."""

from typing import Dict
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from services import ShippingService


class Product:
    """Represents a product in the store."""

    def __init__(self, name, price, available_amount):
        """Initialize product with name, price and available quantity."""
        self.name = name
        self.price = price
        self.available_amount = available_amount

    def is_available(self, requested_amount):
        """Check if requested amount is available."""
        return self.available_amount >= requested_amount

    def buy(self, requested_amount):
        """Purchase requested amount of product if available."""
        if not self.is_available(requested_amount):
            raise ValueError(f"Not enough {self.name} available")
        self.available_amount -= requested_amount

    def __eq__(self, other):
        """Check equality by name."""
        return self.name == other.name

    def __ne__(self, other):
        """Check inequality by name."""
        return self.name != other.name

    def __hash__(self):
        """Hash based on name."""
        return hash(self.name)

    def __str__(self):
        """String representation of the product."""
        return self.name


class ShoppingCart:
    """Represents a shopping cart containing products."""

    products: Dict[Product, int]

    def __init__(self):
        """Initialize empty shopping cart."""
        self.products = {}

    def contains_product(self, product):
        """Check if product is in cart."""
        return product in self.products

    def calculate_total(self):
        """Calculate total price of products in cart."""
        return sum(p.price * count for p, count in self.products.items())

    def add_product(self, product: Product, amount: int):
        """Add product to cart if available in required amount."""
        if not product.is_available(amount):
            raise ValueError(f"Product {product} has only {product.available_amount} items")
        self.products[product] = amount

    def remove_product(self, product):
        """Remove product from cart."""
        if product in self.products:
            del self.products[product]

    def submit_cart_order(self):
        """Buy all products and return their IDs."""
        product_ids = []
        for product, count in self.products.items():
            product.buy(count)
            product_ids.append(str(product))
        self.products.clear()
        return product_ids


@dataclass
class Order:
    """Handles order placement and shipping service interaction."""

    cart: ShoppingCart
    shipping_service: ShippingService
    order_id: str = str(uuid.uuid4())

    def place_order(self, shipping_type, due_date: datetime = None):
        """Place the order and create shipment."""
        if not self.cart.products:
            raise ValueError("Cannot place order with empty cart")
        if not due_date:
            due_date = datetime.now(timezone.utc) + timedelta(seconds=3)
        product_ids = self.cart.submit_cart_order()
        return self.shipping_service.create_shipping(
            shipping_type, product_ids, self.order_id, due_date
        )


@dataclass
class Shipment:
    """Represents shipment and allows status checking."""

    shipping_id: str
    shipping_service: ShippingService

    def check_shipping_status(self):
        """Check shipment status."""
        return self.shipping_service.check_status(self.shipping_id)
