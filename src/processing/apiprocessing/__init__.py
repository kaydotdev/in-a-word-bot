import json
import base64
import logging

import azure.functions as func

from azure.data.tables import UpdateMode
from azure.data.tables.aio import TableServiceClient

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

table_service_client = TableServiceClient.from_connection_string(
    conn_str=REQUEST_STORAGE_CONNECTION_STRING
)

table_client = table_service_client.get_table_client(table_name="requeststates")


async def main(msg: func.QueueMessage) -> None:
    entry_message = msg.get_body()
    user_request_state = {}

    request = base64.b64decode(entry_message).decode('ascii')
    request_payload = json.loads(request)

    logging.info(request_payload)

    try:
        user_request_state = await table_client.get_entity(partition_key=request_payload["PartitionKey"],
                                                           row_key=request_payload["RowKey"])
    except Exception as ex:
        logging.error(ex)
        return

    user_request_state["State"] = "PROCESSING"
    await table_client.upsert_entity(mode=UpdateMode.REPLACE, entity=user_request_state)

    text_to_process, summary_type = user_request_state["Text"], user_request_state["Type"]

    try:
        summary = summary_pipelines[summary_type](text_to_process)
    except Exception as ex:
        logging.error(ex)

        request_headers = {
            "PartitionKey": request_payload["PartitionKey"],
            "RowKey": request_payload["RowKey"],
            "Status": "ERROR"
        }

        message = json.dumps(request_headers).encode('ascii')
        await queue.send_message(base64.b64encode(message))

        return

    user_request_state["State"] = "PROCESSED"
    user_request_state["Text"] = summary

    await table_client.upsert_entity(mode=UpdateMode.REPLACE, entity=user_request_state)

    request_headers = {
        "PartitionKey": request_payload["PartitionKey"],
        "RowKey": request_payload["RowKey"],
        "Status": "SUCCESS"
    }

    message = json.dumps(request_headers).encode('ascii')
    await queue.send_message(base64.b64encode(message))
