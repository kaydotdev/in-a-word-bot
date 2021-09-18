import base64
from json import dumps

from azure.storage.queue.aio import QueueClient
from azure.storage.queue import BinaryBase64EncodePolicy
from azure.storage.blob.aio import BlobServiceClient
from .settings import REQUEST_STORAGE_CONNECTION_STRING


queue = QueueClient.from_connection_string(
    conn_str=REQUEST_STORAGE_CONNECTION_STRING,
    queue_name="summary-batch-processing",
    message_encode_policy=BinaryBase64EncodePolicy()
)

blob_service_client = BlobServiceClient.from_connection_string(
    conn_str=REQUEST_STORAGE_CONNECTION_STRING
)


async def send_to_processing_queue(chat_id: int, text: str, criteria: str):
    request = {
        "chat_id": chat_id,
        "text": text,
        "criteria": criteria,
    }

    message = dumps(request).encode('ascii')
    await queue.send_message(base64.b64encode(message))
