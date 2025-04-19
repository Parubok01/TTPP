import pytest
from app.eshop import Product, ShoppingCart, Order, Shipment
from services import ShippingService
from services.repository import ShippingRepository
from services.publisher import ShippingPublisher
from datetime import datetime, timedelta, timezone
import random


@pytest.fixture
def shipping_service():
    return ShippingService(ShippingRepository(), ShippingPublisher())


def create_cart():
    cart = ShoppingCart()
    cart.add_product(Product("Laptop", 500.0, 10), 1)
    return cart


def test_create_order_success(shipping_service):
    cart = create_cart()
    order = Order(cart, shipping_service)
    shipping_id = order.place_order("Нова Пошта", datetime.now(timezone.utc) + timedelta(seconds=5))
    assert isinstance(shipping_id, str)


def test_order_fails_with_empty_cart(shipping_service):
    cart = ShoppingCart()
    order = Order(cart, shipping_service)
    with pytest.raises(ValueError, match="Cannot place order with empty cart"):
        order.place_order("Нова Пошта")


def test_invalid_shipping_type_raises(shipping_service):
    cart = create_cart()
    order = Order(cart, shipping_service)
    with pytest.raises(ValueError, match="Shipping type is not available"):
        order.place_order("Космічна доставка")


def test_due_date_in_past_fails(shipping_service):
    cart = create_cart()
    order = Order(cart, shipping_service)
    with pytest.raises(ValueError, match="Shipping due datetime must be greater than datetime now"):
        order.place_order("Нова Пошта", datetime.now(timezone.utc) - timedelta(minutes=1))


def test_shipping_status_created_and_updated(shipping_service):
    cart = create_cart()
    order = Order(cart, shipping_service)
    due_date = datetime.now(timezone.utc) + timedelta(seconds=5)
    shipping_id = order.place_order("Нова Пошта", due_date)

    status = shipping_service.check_status(shipping_id)
    assert status == ShippingService.SHIPPING_IN_PROGRESS


def test_shipping_completion_logic(shipping_service):
    cart = create_cart()
    order = Order(cart, shipping_service)
    shipping_id = order.place_order("Нова Пошта", datetime.now(timezone.utc) + timedelta(minutes=1))

    result = shipping_service.complete_shipping(shipping_id)
    assert result["HTTPStatusCode"] == 200


def test_fail_shipping_logic(shipping_service):
    cart = create_cart()
    order = Order(cart, shipping_service)
    shipping_id = order.place_order("Нова Пошта", datetime.now(timezone.utc) + timedelta(minutes=1))

    result = shipping_service.fail_shipping(shipping_id)
    assert result["HTTPStatusCode"] == 200


def test_poll_shipping_batch_returns_list(shipping_service):
    cart = create_cart()
    order = Order(cart, shipping_service)
    order.place_order("Нова Пошта", datetime.now(timezone.utc) + timedelta(minutes=1))

    result = shipping_service.process_shipping_batch()
    assert isinstance(result, list)


def test_shipment_check_status(shipping_service):
    cart = create_cart()
    order = Order(cart, shipping_service)
    shipping_id = order.place_order("Нова Пошта", datetime.now(timezone.utc) + timedelta(minutes=1))

    shipment = Shipment(shipping_id, shipping_service)
    status = shipment.check_shipping_status()
    assert status == ShippingService.SHIPPING_IN_PROGRESS


def test_multiple_orders_integration(shipping_service):
    cart1 = create_cart()
    cart2 = create_cart()

    order1 = Order(cart1, shipping_service)
    order2 = Order(cart2, shipping_service)

    shipping_id1 = order1.place_order("Укр Пошта", datetime.now(timezone.utc) + timedelta(minutes=2))
    shipping_id2 = order2.place_order("Meest Express", datetime.now(timezone.utc) + timedelta(minutes=2))

    assert shipping_id1 != shipping_id2
    
def test_cart_integration():
    cart = ShoppingCart()
    products = [
        Product("Book", 10.0, 2),
        Product("Pen", 1.5, 5)
    ]
    
    # Додаємо продукти
    cart.add_product(products[0], 1)
    cart.add_product(products[1], 3)
    
    # Перевіряємо наявність і загальну суму
    assert cart.contains_product(products[0])
    assert cart.calculate_total() == 10.0 * 1 + 1.5 * 3
    
    # Видаляємо один продукт
    cart.remove_product(products[0])
    assert not cart.contains_product(products[0])
    assert cart.calculate_total() == 1.5 * 3

def test_add_product_success():
    cart = ShoppingCart()
    product = Product("Notebook", 5.99, 5)
    
    # Успішне додавання
    cart.add_product(product, 3)
    assert cart.contains_product(product)
    assert cart.products[product] == 3

def test_add_product_failure():
    cart = ShoppingCart()
    product = Product("Notebook", 5.99, 2)
    
    # Спроба додати більше, ніж є в наявності
    with pytest.raises(ValueError) as exc_info:
        cart.add_product(product, 3)
    assert str(exc_info.value) == "Product Notebook has only 2 items"
    
def test_contains_product():
    cart = ShoppingCart()
    product = Product("Book", 15.99, 10)
    
    # Перевірка порожнього кошика
    assert not cart.contains_product(product)
    
    # Додаємо продукт і перевіряємо знову
    cart.add_product(product, 2)
    assert cart.contains_product(product)