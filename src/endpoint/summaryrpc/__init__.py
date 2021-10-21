import re
import json
import base64
import logging

import azure.functions as func

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text, code

from azure.data.tables.aio import TableServiceClient

from ..apiendpoint.bot import bot_instance, dispatcher_instance
from ..apiendpoint.settings import MAX_MESSAGE_LENGTH, REQUEST_STORAGE_CONNECTION_STRING


re_strip_uuid = re.compile(r"[-]+")
re_clean_summary = re.compile(r"[^0-9a-zA-Z',.!?\n\t -]+")


table_service_client = TableServiceClient.from_connection_string(
    conn_str=REQUEST_STORAGE_CONNECTION_STRING
)

table_client = table_service_client.get_table_client(table_name="requeststates")


async def main(msg: func.QueueMessage) -> None:
    user_request_state = {}

    request = base64.b64decode(msg.get_body()).decode('ascii')
    request_payload = json.loads(request)

    try:
        user_request_state = await table_client.get_entity(partition_key=request_payload["PartitionKey"],
                                                        row_key=request_payload["RowKey"])
    except Exception as ex:
        logging.error(ex)
        return

    chat_id = user_request_state["RowKey"]
    requested_summary = re_clean_summary.sub('', user_request_state["Text"])

    await table_client.delete_entity(partition_key=request_payload["PartitionKey"], row_key=request_payload["RowKey"])

    Bot.set_current(bot_instance)
    Dispatcher.set_current(dispatcher_instance)

    if request_payload["Status"] == "SUCCESS":
        ready_message = text(*[
            "Your ", code(user_request_state['Type']), " request ", code(re_strip_uuid.sub('', user_request_state['PartitionKey'])), " is ready:"
        ], sep='')

        await bot_instance.send_message(chat_id, ready_message, parse_mode=ParseMode.MARKDOWN)

        for i in range(0, len(requested_summary), MAX_MESSAGE_LENGTH):
            await bot_instance.send_message(chat_id, requested_summary[i:i + MAX_MESSAGE_LENGTH],
                                    disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)

        logging.info(f"Successfully sent to the client summary: {user_request_state}")
    else:
        PROCESSING_ERROR_MESSAGE = emojize(text(*[
            ":warning:", "An error occured during text processing! Try different format or contact maintainer!"
        ], sep=' '))

        await bot_instance.send_message(chat_id, PROCESSING_ERROR_MESSAGE, parse_mode=ParseMode.MARKDOWN)
