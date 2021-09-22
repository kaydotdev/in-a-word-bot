import re
import base64

from json import dumps
from uuid import uuid4
from datetime import datetime

from aiostream.stream import list as aiolist
from azure.data.tables.aio import TableServiceClient

from azure.storage.queue.aio import QueueClient
from azure.storage.queue import BinaryBase64EncodePolicy
from azure.storage.blob.aio import BlobServiceClient
from .settings import REQUEST_STORAGE_CONNECTION_STRING


re_strip_uuid = re.compile(r"[-]+")


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
    request = { **request_headers, 'Text': text, 'Type': criteria, 'State': 'PENDING', 'UnixTimeStamp': int(datetime.timestamp(datetime.now())) }

    await table_client.create_entity(entity=request)

    message = dumps(request_headers).encode('ascii')
    await queue.send_message(base64.b64encode(message))


async def __get_user_request__(chat_id: int):
    parameters = { "chat_id": str(chat_id) }
    return await aiolist(table_client.query_entities("RowKey eq @chat_id", parameters=parameters))


async def check_if_in_queue(chat_id: int):
    return len(await __get_user_request__(chat_id)) > 0


async def get_request_info(chat_id: int):
    return next(iter(await __get_user_request__(chat_id) or []), None)


async def get_requests_count_in_front(chat_id: int):
    user_request = await get_request_info(chat_id)

    if user_request is None:
        return None

    parameters = { "timestamp": int(user_request.get('UnixTimeStamp', 0)) }
    request_in_front = await aiolist(table_client.query_entities("UnixTimeStamp lt @timestamp", parameters=parameters))

    return {
        "request_id": user_request.get('PartitionKey', None),
        "request_state": user_request.get('State', 'UNKNOWN'),
        "request_count_in_front": len(request_in_front)
    }


async def abort_request(chat_id: int):
    user_request = await get_request_info(chat_id)

    if user_request is None:
        return "no-requests"
    elif user_request["State"] != "PENDING":
        return "in-processing"
    else:  
        await table_client.delete_entity(row_key=user_request["RowKey"],
                                        partition_key=user_request["PartitionKey"])
        return "ok"
