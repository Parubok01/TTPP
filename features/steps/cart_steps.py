from behave import given, when, then
from eshop import Product, ShoppingCart, Order

@given("The product has availability of {availability}")
def create_product_for_cart(context, availability):
    context.product = Product(name="any", price=123, available_amount=int(availability))

@given('An empty shopping cart')
def empty_cart(context):
    context.cart = ShoppingCart()

@given("A product with availability of {availability}")
def create_product(context, availability):
    context.product = Product(name="test_product", price=100, available_amount=int(availability))

@given("Two products with same name")
def create_same_products(context):
    context.product1 = Product(name="same_name", price=100, available_amount=100)
    context.product2 = Product(name="same_name", price=200, available_amount=200)

@given("Two products with different names")
def create_different_products(context):
    context.product1 = Product(name="product1", price=100, available_amount=100)
    context.product2 = Product(name="product2", price=200, available_amount=200)

@when("I add product to the cart in amount {product_amount}")
def add_product(context, product_amount):
    try:
        context.cart.add_product(context.product, int(product_amount))
        context.add_successfully = True
    except ValueError:
        context.add_successfully = False

@when("I try to add product with invalid amount")
def add_product_invalid_amount(context):
    try:
        context.cart.add_product(context.product, None)
        context.add_successfully = True
    except (ValueError, TypeError):
        context.add_successfully = False

@when("I try to add None product to cart")
def add_none_product(context):
    try:
        context.cart.add_product(None, 1)
        context.add_successfully = True
    except (ValueError, TypeError):
        context.add_successfully = False

@when("I remove the product from cart")
def remove_product(context):
    context.cart.remove_product(context.product)

@when("I add another product to the cart in amount {amount}")
def add_another_product(context, amount):
    context.second_product = Product(name="another", price=100, available_amount=100)
    context.cart.add_product(context.second_product, int(amount))

@when("I submit the order")
def submit_order(context):
    context.order = Order(context.cart)
    context.order.place_order()

@when("I check availability for amount {amount}")
def check_availability(context, amount):
    context.is_available = context.product.is_available(int(amount))

@when("I buy {amount} units")
def buy_units(context, amount):
    try:
        context.product.buy(int(amount))
        context.operation_successful = True
    except ValueError:
        context.operation_successful = False

@when("I try to buy {amount} units")
def try_buy_units(context, amount):
    try:
        context.product.buy(int(amount))
        context.operation_successful = True
    except ValueError:
        context.operation_successful = False

@when("I compare them")
def compare_products(context):
    context.are_equal = context.product1 == context.product2

@then("Product is added to the cart successfully")
def add_successful(context):
    assert context.add_successfully == True

@then("Product is not added to cart successfully")
def add_failed(context):
    assert context.add_successfully == False

@then("The cart should be empty")
def cart_empty(context):
    assert len(context.cart.products) == 0

@then("The total price should be {expected_price}")
def check_total_price(context, expected_price):
    assert context.cart.calculate_total() == int(expected_price)

@then("The cart should contain {count} products")
def check_cart_products_count(context, count):
    assert len(context.cart.products) == int(count)

@then("The product availability should be {expected_amount}")
def check_product_availability(context, expected_amount):
    assert context.product.available_amount == int(expected_amount)

@then("The product should be available")
def product_available(context):
    assert context.is_available == True

@then("The product should not be available")
def product_not_available(context):
    assert context.is_available == False

@then("The operation should fail")
def operation_failed(context):
    assert context.operation_successful == False

@then("They should be equal")
def products_equal(context):
    assert context.are_equal == True

@then("They should not be equal")
def products_not_equal(context):
    assert context.are_equal == False 