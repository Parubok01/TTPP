import uuid
import boto3
from app.eshop import Product, ShoppingCart, Order, Shipment
import random
from services import ShippingService
from services.repository import ShippingRepository
from services.publisher import ShippingPublisher
from datetime import datetime, timedelta, timezone
from services.config import AWS_ENDPOINT_URL, AWS_REGION, SHIPPING_QUEUE
import pytest

@pytest.mark.parametrize("order_id, shipping_id", [
    ("order_1", "shipping_1"),
    ("order_i2hur2937r9", "shipping_1!!!!"),
    (8662354, 123456),
    (str(uuid.uuid4()), str(uuid.uuid4()))
])
def test_place_order_with_mocked_repo(mocker, order_id, shipping_id):
    # Mock entire boto3 and db module to prevent any AWS calls
    mocker.patch('boto3.resource')
    mocker.patch('boto3.client')
    mocker.patch('services.db.get_dynamodb_resource')
    
    mock_repo = mocker.Mock()
    mock_publisher = mocker.Mock()
    shipping_service = ShippingService(mock_repo, mock_publisher)
    mock_repo.create_shipping.return_value = shipping_id
    cart = ShoppingCart()
    cart.add_product(Product(
        available_amount=10,
        name='Product',
        price=random.random() * 10000), 
        amount=9
    )
    order = Order(cart, shipping_service, order_id)
    due_date = datetime.now(timezone.utc) + timedelta(seconds=3)
    actual_shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=due_date
    )
    assert actual_shipping_id == shipping_id, "Actual shipping id must be equal to mock return value"
    mock_repo.create_shipping.assert_called_with(
        ShippingService.list_available_shipping_type()[0], 
        ["Product"], 
        order_id, 
        shipping_service.SHIPPING_CREATED, 
        due_date
    )
    mock_publisher.send_new_shipping.assert_called_with(shipping_id)

def test_place_order_with_unavailable_shipping_type_fails(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product(
        available_amount=10,
        name='Product',
        price=random.random() * 10000), 
        amount=9
    )
    order = Order(cart, shipping_service)
    shipping_id = None
    with pytest.raises(ValueError) as excinfo:
        shipping_id = order.place_order(
            "Новий тип доставки",
            due_date=datetime.now(timezone.utc) + timedelta(seconds=3)
        )
    assert shipping_id is None, "Shipping id must not be assigned"
    assert "Shipping type is not available" in str(excinfo.value)

def test_when_place_order_then_shipping_in_queue(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product(
        available_amount=10,
        name='Product',
        price=random.random() * 10000), 
        amount=9
    )
    order = Order(cart, shipping_service)
    shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    sqs_client = boto3.client(
        "sqs",
        endpoint_url=AWS_ENDPOINT_URL,
        region_name=AWS_REGION,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )
    queue_url = sqs_client.get_queue_url(QueueName=SHIPPING_QUEUE)["QueueUrl"]
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    messages = response.get("Messages", [])
    assert len(messages) == 1, "Expected 1 SQS message"
    body = messages[0]["Body"]
    assert shipping_id == body

def test_check_shipping_status_after_order_placement(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product(available_amount=10, name='TestProduct', price=100.0), amount=5)
    order = Order(cart, shipping_service)
    shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    shipment = Shipment(shipping_id, shipping_service)
    status = shipment.check_shipping_status()
    assert status == shipping_service.SHIPPING_IN_PROGRESS, "Shipping status should be 'in progress' after order placement"

def test_process_shipping_batch_completes_valid_shipping(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product(available_amount=10, name='TestProduct', price=100.0), amount=5)
    order = Order(cart, shipping_service)
    shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    results = shipping_service.process_shipping_batch()
    assert len(results) == 1, "Expected one shipping processed"
    status = shipping_service.check_status(shipping_id)
    assert status == shipping_service.SHIPPING_COMPLETED, "Shipping should be completed"

def test_process_shipping_batch_fails_expired_shipping(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product(available_amount=10, name='TestProduct', price=100.0), amount=5)
    order = Order(cart, shipping_service)
    shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) - timedelta(minutes=1)
    )
    results = shipping_service.process_shipping_batch()
    assert len(results) == 1, "Expected one shipping processed"
    status = shipping_service.check_status(shipping_id)
    assert status == shipping_service.SHIPPING_FAILED, "Expired shipping should be failed"

def test_place_order_with_empty_cart_fails(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    order = Order(cart, shipping_service)
    shipping_id = None
    try:
        shipping_id = order.place_order(
            ShippingService.list_available_shipping_type()[0],
            due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
        )
    except Exception:
        pass
    assert shipping_id is None, "Should not assign shipping_id for empty cart"

def test_multiple_orders_create_multiple_shippings(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart1 = ShoppingCart()
    cart1.add_product(Product(available_amount=10, name='Product1', price=100.0), amount=5)
    cart2 = ShoppingCart()
    cart2.add_product(Product(available_amount=10, name='Product2', price=200.0), amount=3)
    order1 = Order(cart1, shipping_service)
    order2 = Order(cart2, shipping_service)
    shipping_id1 = order1.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    shipping_id2 = order2.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    assert shipping_id1 != shipping_id2, "Shipping IDs should be unique"
    status1 = shipping_service.check_status(shipping_id1)
    status2 = shipping_service.check_status(shipping_id2)
    assert status1 == shipping_service.SHIPPING_IN_PROGRESS
    assert status2 == shipping_service.SHIPPING_IN_PROGRESS

def test_shipping_status_persists_in_dynamodb(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product(available_amount=10, name='TestProduct', price=100.0), amount=5)
    order = Order(cart, shipping_service)
    shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    repo = ShippingRepository()
    shipping_item = repo.get_shipping(shipping_id)
    assert shipping_item['shipping_status'] == shipping_service.SHIPPING_IN_PROGRESS
    assert shipping_item['shipping_type'] == ShippingService.list_available_shipping_type()[0]

def test_invalid_due_date_fails_order_placement(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product(available_amount=10, name='TestProduct', price=100.0), amount=5)
    order = Order(cart, shipping_service)
    with pytest.raises(ValueError) as excinfo:
        order.place_order(
            ShippingService.list_available_shipping_type()[0],
            due_date=datetime.now(timezone.utc) - timedelta(minutes=1)
        )
    assert "Shipping due datetime must be greater than datetime now" in str(excinfo.value)

def test_shipping_queue_receives_multiple_messages(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart1 = ShoppingCart()
    cart1.add_product(Product(available_amount=10, name='Product1', price=100.0), amount=5)
    cart2 = ShoppingCart()
    cart2.add_product(Product(available_amount=10, name='Product2', price=200.0), amount=3)
    order1 = Order(cart1, shipping_service)
    order2 = Order(cart2, shipping_service)
    shipping_id1 = order1.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    shipping_id2 = order2.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    sqs_client = boto3.client(
        "sqs",
        endpoint_url=AWS_ENDPOINT_URL,
        region_name=AWS_REGION,
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )
    queue_url = sqs_client.get_queue_url(QueueName=SHIPPING_QUEUE)["QueueUrl"]
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10
    )
    messages = response.get("Messages", [])
    assert len(messages) == 2, "Expected 2 SQS messages"
    bodies = [msg["Body"] for msg in messages]
    assert shipping_id1 in bodies
    assert shipping_id2 in bodies

def test_complete_shipping_manually(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product(available_amount=10, name='TestProduct', price=100.0), amount=5)
    order = Order(cart, shipping_service)
    shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    shipping_service.complete_shipping(shipping_id)
    status = shipping_service.check_status(shipping_id)
    assert status == shipping_service.SHIPPING_COMPLETED

def test_fail_shipping_manually(dynamo_resource):
    shipping_service = ShippingService(ShippingRepository(), ShippingPublisher())
    cart = ShoppingCart()
    cart.add_product(Product(available_amount=10, name='TestProduct', price=100.0), amount=5)
    order = Order(cart, shipping_service)
    shipping_id = order.place_order(
        ShippingService.list_available_shipping_type()[0],
        due_date=datetime.now(timezone.utc) + timedelta(minutes=1)
    )
    shipping_service.fail_shipping(shipping_id)
    status = shipping_service.check_status(shipping_id)
    assert status == shipping_service.SHIPPING_FAILED