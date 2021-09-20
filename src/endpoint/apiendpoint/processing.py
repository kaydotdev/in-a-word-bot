import base64

from json import dumps
from uuid import uuid4

from azure.data.tables.aio import TableServiceClient

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

table_service_client = TableServiceClient.from_connection_string(
    conn_str=REQUEST_STORAGE_CONNECTION_STRING
)

table_client = table_service_client.get_table_client(table_name="requeststates")


async def send_to_processing_queue(chat_id: int, text: str, criteria: str):
    request_headers = { "PartitionKey": str(uuid4()), "RowKey": str(chat_id) }
    request = { **request_headers, 'Text': text, 'Type': criteria, 'State': 'PENDING' }

    await table_client.create_entity(entity=request)

    message = dumps(request).encode('ascii')
    await queue.send_message(base64.b64encode(message))


async def check_if_in_queue(chat_id: int):
    parameters = { "chat_id": str(chat_id) }
    records = table_client.query_entities("RowKey eq @chat_id", parameters=parameters)

    return len([1 async for _ in records]) > 0
