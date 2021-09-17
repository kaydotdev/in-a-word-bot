import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from .settings import API_TOKEN, MONGO_CONNECTION_URL


loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

bot_instance = Bot(token=API_TOKEN, loop=loop)

storage = MongoStorage(uri=MONGO_CONNECTION_URL, db_name='in_a_word_bot_fsm')
dispatcher_instance = Dispatcher(bot_instance, storage=storage)


class DialogFSM(StatesGroup):
    main_menu = State()
    content_type_selection = State()
    summary_type_selection = State()

    plain_text_processing = State()
    file_processing = State()
    web_resource_processing = State()
