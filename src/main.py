import io
import re
import asyncio
import logging

import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import start_webhook, start_polling

from datetime import datetime

from processing.transformer import SummaryTransformer
from processing.tfidf import summary as extractive_summary
from static import *
from settings import *
from utils import remove_html_tags, normalize_http_response,\
                   re_file_format, re_match_http_url


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop)

storage = RedisStorage2(REDIS_HOST, REDIS_PORT, db=REDIS_DB)
dispatcher = Dispatcher(bot, storage=storage)

transformer = SummaryTransformer(text_preprocessor_file=TOKENIZER_FILE, model_state_dict_file=TRANSFORMER_STATE_DICT_FILE)

extraction_lock = asyncio.Lock()


class DialogFSM(StatesGroup):
    content_type_selection = State()
    summary_type_selection = State()

    plain_text_processing = State()
    file_processing = State()
    web_resource_processing = State()


async def extract_summary(message: types.Message, state: FSMContext, text: str):
    async with state.proxy() as data:

        # Summary extraction is a heavy in computation and blocking, so should be bound with mutex
        async with extraction_lock:
            if data['SUMMARY_TYPE'] == SUMMARIZE_EXTRACTIVE_OPTION or len(text) > MAX_ABSTRACT_LENGTH:
                summary = extractive_summary(text, type="max")
            else:
                summary = transformer.generate(text)

            await state.finish()
            await message.answer(summary, parse_mode=ParseMode.MARKDOWN,
                                disable_web_page_preview=True, reply_markup=empty_keyboard)


@dispatcher.message_handler(commands=['cancel'], state='*')
async def handle_cancel(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_cancel")

    if await state.get_state() is None:
        return

    await state.finish()
    await message.answer(COMMAND_CANCELLED, parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True, reply_markup=empty_keyboard)


@dispatcher.message_handler(commands=['start'], state='*')
async def handle_start(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_start")

    await message.answer(BOT_TITLE, parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True, reply_markup=empty_keyboard)


@dispatcher.message_handler(commands=['docs'], state='*')
async def handle_start(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_docs")

    await message.answer(USAGE_GUIDE, parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)


@dispatcher.message_handler(commands=['summary'], state='*')
async def handle_start(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_summary")

    await DialogFSM.content_type_selection.set()
    await message.answer(CHOOSE_AVAILABLE_OPTIONS, parse_mode=ParseMode.MARKDOWN,
                         reply_markup=summary_content_option_keyboard)


@dispatcher.message_handler(lambda message: message.text in SUMMARY_CONTENT_OPTIONS, state=DialogFSM.content_type_selection)
async def handle_summary_type_assignment(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_summary_type_assignment")

    async with state.proxy() as data:
        data['USER_DATA_TYPE'] = message.text

        await DialogFSM.summary_type_selection.set()
        await message.answer(SUMMARY_OPTION_TITLE, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=summary_type_option_keyboard)


@dispatcher.message_handler(lambda message: message.text in SUMMARY_TYPE_OPTIONS, state=DialogFSM.summary_type_selection)
async def handle_user_data_source_input(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_user_data_source_input")

    async with state.proxy() as data:
        data['SUMMARY_TYPE'] = message.text

        if data['USER_DATA_TYPE'] == SUMMARY_FROM_PLAIN_TEXT_OPTION:
            await DialogFSM.plain_text_processing.set()
        elif data['USER_DATA_TYPE'] == SUMMARY_FROM_FILE_OPTION:
            await DialogFSM.file_processing.set()
        elif data['USER_DATA_TYPE'] == SUMMARY_FROM_WEB_RESOURCE_OPTION:
            await DialogFSM.web_resource_processing.set()
        else:
            await state.finish()

        await message.answer(CHOSEN_SUMMARY_RESPONSES.get(data['USER_DATA_TYPE']),
                             parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)


@dispatcher.message_handler(state=DialogFSM.plain_text_processing, content_types=[ContentType.TEXT])
async def handle_plain_text_summary(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_plain_text_summary")

    await extract_summary(message, state, message.text)


@dispatcher.message_handler(state=DialogFSM.file_processing, content_types=[ContentType.DOCUMENT])
async def handle_file_summary(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_file_summary")

    if message.document.file_size > MAX_FILE_SIZE:
        await message.answer(FILE_SIZE_EXCEEDED_LIMIT_ERROR, parse_mode=ParseMode.MARKDOWN)
    elif re.match(re_file_format, message.document.file_name) is None:
        await message.answer(FILE_WRONG_EXTENSION_ERROR, parse_mode=ParseMode.MARKDOWN)
    else:
        try:
            await message.answer(PROCESSING_FILE, disable_web_page_preview=True)
            logging.info(f"[{datetime.now()}@{message.from_user.username}] processing file '{message.document.file_name}'")

            file: io.BytesIO = await bot.download_file_by_id(message.document.file_id)
            file_containment = file.read().decode('utf-8')
            file.close()

            await extract_summary(message, state, file_containment)
        except Exception as ex:
            logging.error(f"[{datetime.now()}@bot] Failed to open file: {ex}")

            await state.finish()
            await message.answer(FILE_OPEN_ERROR, parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)


@dispatcher.message_handler(state=DialogFSM.web_resource_processing, content_types=[ContentType.TEXT])
async def handle_web_resource_summary(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_web_resource_summary")

    if re.match(re_match_http_url, message.text) is None:
        await message.answer(INCORRECT_HTTP_FORMAT_ERROR, parse_mode=ParseMode.MARKDOWN)
    else:
        try:
            await message.answer(SENDING_REQUEST, parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)

            async with aiohttp.ClientSession() as session:
                async with session.get(message.text) as response:
                    response_body = await response.text()

            await extract_summary(message, state,
                normalize_http_response(
                    remove_html_tags(response_body)
                )
            )
        except Exception as ex:
            logging.error(f"[{datetime.now()}@bot] Failed to parse web resource content: {ex}")

            await state.finish()
            await message.answer(WEB_CRAWLER_HTTP_ERROR, parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)


async def on_startup(dp):
    logging.info(f'[{datetime.now()}@bot] Initiating startup...')

    await bot.set_webhook(WEBHOOK_URL)

    logging.info(f'[{datetime.now()}@bot] Startup successful!')


async def on_shutdown(dp):
    logging.info(f'[{datetime.now()}@bot] Initiating shutdown...')

    if WEBHOOK_MODE:
        await bot.delete_webhook()

    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

    logging.info(f'[{datetime.now()}@bot] Shutdown successful!')


async def app():
    app = get_new_configured_app(dispatcher=dispatcher, path=WEBHOOK_PATH)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == '__main__':
    if WEBHOOK_MODE:
        start_webhook(
            dispatcher=dispatcher,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        start_polling(dispatcher=dispatcher,
                      skip_updates=True,
                      on_shutdown=on_shutdown)
