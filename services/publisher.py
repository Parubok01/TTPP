import boto3
from .config import AWS_ENDPOINT_URL, AWS_REGION, SHIPPING_QUEUE

class ShippingPublisher:
    def __init__(self):
        self._client = None
        self._queue_url = None
    
    @property
    def client(self):
        if self._client is None:
            self._client = boto3.client(
                "sqs",
                endpoint_url=AWS_ENDPOINT_URL,
                region_name=AWS_REGION,
                aws_access_key_id="test",
                aws_secret_access_key="test",
            )
        return self._client
    
    @property
    def queue_url(self):
        if self._queue_url is None:
            response = self.client.create_queue(QueueName=SHIPPING_QUEUE)
            self._queue_url = response["QueueUrl"]
        return self._queue_url
    
    def send_new_shipping(self, shipping_id: str):
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=shipping_id
        )
        return response['MessageId']
    
    def poll_shipping(self, batch_size: int = 10):
        messages = self.client.receive_message(
            QueueUrl=self.queue_url,
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=batch_size,
            WaitTimeSeconds=10
        )
        if 'Messages' not in messages:
            return []
        return [msg['Body'] for msg in messages['Messages']]