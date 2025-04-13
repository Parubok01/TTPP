from behave import given, when, then
from eshop import Product

@given('A product "{name}" with price {price} and availability {availability}')
def step_given_product(context, name, price, availability):
    context.product = Product(name=name, price=float(price), available_amount=int(availability))

@given('No product is defined')
def step_no_product(context):
    context.product = None

@given('A product with None availability')
def step_product_none_availability(context):
    context.product = Product(name="Undefined", price=100, available_amount=None)

@given('A product with string availability "{availability}"')
def step_product_string_availability(context, availability):
    try:
        context.product = Product(name="Stringy", price=100, available_amount=availability)
    except Exception as e:
        context.product = None

@when('I check availability for {requested}')
def step_check_availability(context, requested):
    try:
        if context.product:
            context.result = context.product.is_available(int(requested))
        else:
            context.result = None
    except:
        context.result = None

@then('The product is available')
def step_then_available(context):
    assert context.result is True

@then('The product is not available')
def step_then_not_available(context):
    assert context.result is False

@then('The product check fails')
def step_check_failed(context):
    assert context.result is None
