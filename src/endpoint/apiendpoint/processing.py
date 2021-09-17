from json import dumps

from azure.storage.queue.aio import QueueClient
from .settings import REQUEST_STORAGE_CONNECTION_STRING


queue = QueueClient.from_connection_string(
    conn_str=REQUEST_STORAGE_CONNECTION_STRING,
    queue_name="summary-batch-processing"
)


async def send_to_processing_queue(chat_id: int, text: str, criteria: str):
    request = {
        "chat_id": chat_id,
        "text": text,
        "criteria": criteria,
    }

    await queue.send_message(dumps(request))
