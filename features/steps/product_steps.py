from behave import given, when, then
from eshop import Product

@given("I try to create a product with zero price")
def create_product_zero_price(context):
    context.product = Product(name="zero_price", price=0, available_amount=100)

@given("I try to create a product with negative price")
def create_product_negative_price(context):
    context.product = Product(name="negative_price", price=-100, available_amount=100)

@when("The product is created")
def product_created(context):
    context.creation_successful = True

@then("The price should be 0")
def check_zero_price(context):
    assert context.product.price == 0

@then("The price should be negative")
def check_negative_price(context):
    assert context.product.price < 0 