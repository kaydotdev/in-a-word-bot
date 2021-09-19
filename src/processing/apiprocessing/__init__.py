import json
import base64
import logging

import azure.functions as func

from json import dumps

from azure.storage.queue.aio import QueueClient
from azure.storage.queue import BinaryBase64EncodePolicy

from .extractive import extractive_summary
from .settings import THRESHOLD_MULTIPLYER, REQUEST_STORAGE_CONNECTION_STRING


summary_pipelines = {
    'Extractive': lambda text: extractive_summary(text, THRESHOLD_MULTIPLYER),
    'Abstractive': lambda text: extractive_summary(text, THRESHOLD_MULTIPLYER) # TODO: Implement abstractive summarization with transformers
}

queue = QueueClient.from_connection_string(
    conn_str=REQUEST_STORAGE_CONNECTION_STRING,
    queue_name="summary-return-result",
    message_encode_policy=BinaryBase64EncodePolicy()
)


async def main(msg: func.QueueMessage) -> None:
    request = base64.b64decode(msg.get_body()).decode('ascii')
    request_payload = json.loads(request)

    chat_id = request_payload.get('chat_id', None)
    text_to_process = request_payload.get('text', '')
    summary_type = request_payload.get('criteria', None)

    logging.info(dumps({ "chat_id": chat_id, "criteria": summary_type }))

    summary = summary_pipelines[summary_type](text_to_process)

    queue_response = {
        "chat_id": chat_id,
        "summary": summary,
        "criteria": summary_type
    }

    message = dumps(queue_response).encode('ascii')
    await queue.send_message(base64.b64encode(message))
