import json
import base64
import logging

import azure.functions as func

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from ..apiendpoint.bot import bot_instance, dispatcher_instance


async def main(msg: func.QueueMessage) -> None:
    request = base64.b64decode(msg.get_body()).decode('ascii')
    request_payload = json.loads(request)

    chat_id = request_payload.get('chat_id', '')
    requested_summary = request_payload.get('summary', '')

    Bot.set_current(bot_instance)
    Dispatcher.set_current(dispatcher_instance)

    await bot_instance.send_message(chat_id, requested_summary, parse_mode=ParseMode.MARKDOWN)

    logging.info(f"Successfully sent to the client summary: {request_payload}")
