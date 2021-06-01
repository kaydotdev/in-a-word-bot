import re
import logging
import aiohttp

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, ContentType
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from datetime import datetime
from static_content import *
from settings import *
from states import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
cache_storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=cache_storage)

if WEBHOOK_ENABLED:
    WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"


@dispatcher.message_handler(commands=['cancel'], state='*')
async def handle_cancel(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_cancel")
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.finish()
    await message.answer(f'The command has been cancelled.', reply_markup=empty_keyboard)


@dispatcher.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_start")

    await DialogFSM.main_menu.set()
    await message.answer(BOT_TITLE, parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True, reply_markup=main_menu_keyboard)


@dispatcher.message_handler(lambda message: message.text in MAIN_MENU_OPTIONS,
                            state=DialogFSM.main_menu)
async def handle_summarization_criteria_assignment(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_summarization_criteria_assignment")

    async with state.proxy() as data:
        data['USER_DATA_TYPE'] = message.text

        await DialogFSM.summarization_criteria.set()
        await message.answer(SUMMARY_OPTION_TITLE, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=summarize_by_criteria_keyboard)


@dispatcher.message_handler(lambda message: message.text in SUMMARIZE_BY_CRITERIA_OPTIONS,
                            state=DialogFSM.summarization_criteria)
async def handle_user_data_source_input(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_user_data_source_input")

    async with state.proxy() as data:
        data['SUMMARIZATION_CRITERIA_TYPE'] = message.text

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

    async with state.proxy() as data:
        generated_summary = await text_summary_async(message.text, data['SUMMARIZATION_CRITERIA_TYPE'])

        await state.finish()
        await DialogFSM.main_menu.set()

        # Max length of single Telegram message is 4096 characters. If gathered
        # text contains more symbols, it will be split into chunks of MAX_MESSAGE_LENGTH
        # and delivered in sequence
        for i in range(0, len(generated_summary), MAX_MESSAGE_LENGTH):
            await message.answer(generated_summary[i:i + MAX_MESSAGE_LENGTH],
                                 disable_web_page_preview=True,
                                 reply_markup=main_menu_keyboard)


@dispatcher.message_handler(lambda message: re.match(r'/[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,'
                                                     r'6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g',
                                                     message.text) is not None,
                            state=DialogFSM.web_resource_processing, content_types=[ContentType.TEXT])
async def handle_web_resource_summary(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_web_resource_summary")

    async with state.proxy() as data:
        try:
            await message.answer(SENDING_REQUEST, parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)

            async with aiohttp.ClientSession() as session:
                async with session.get(message.text) as response:
                    response_body = await response.text()

            generated_summary = await text_summary_async(response_body, data['SUMMARIZATION_CRITERIA_TYPE'])

            await state.finish()
            await DialogFSM.main_menu.set()

            for i in range(0, len(generated_summary), MAX_MESSAGE_LENGTH):
                await message.answer(generated_summary[i:i + MAX_MESSAGE_LENGTH],
                                     disable_web_page_preview=True,
                                     reply_markup=main_menu_keyboard)
        except Exception as ex:
            logging.error(f"[{datetime.now()}@bot] Failed to parse web resource content: {ex}")

            await state.finish()
            await DialogFSM.main_menu.set()
            await message.answer(WEB_CRAWLER_HTTP_ERROR, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu_keyboard)


async def text_summary_async(entry_text: str, criteria: str):
    if criteria == SUMMARIZE_BY_FREQUENCY_OPTION:
        return entry_text
    elif criteria == SUMMARIZE_BY_ABSTRACTION_OPTION:
        return entry_text
    else:
        return NO_SUMMARIZATION_CRITERIA_ERROR


async def shutdown_storage(_dispatcher):
    logging.warning(f'[{datetime.now()}@bot] waiting for storage to shutdown')
    await _dispatcher.storage.close()
    await _dispatcher.storage.wait_closed()


async def on_startup(_dispatcher):
    logging.warning(f'[{datetime.now()}@bot] setting web hook on {WEBHOOK_URL}')
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(_dispatcher):
    logging.warning(f'[{datetime.now()}@bot] deleting web hook')
    await bot.delete_webhook()
    await shutdown_storage(_dispatcher)
    logging.warning(f'[{datetime.now()}@bot] bot was successfully shut down')


async def on_polling_shutdown(_dispatcher):
    await shutdown_storage(_dispatcher)
    logging.warning(f'[{datetime.now()}@bot] bot was successfully shut down')


if __name__ == '__main__':
    if WEBHOOK_ENABLED:
        executor.start_webhook(dispatcher,
                               WEBHOOK_PATH,
                               on_startup=on_startup,
                               on_shutdown=on_shutdown,
                               skip_updates=True,
                               host=WEBHOOK_IP,
                               port=WEBHOOK_PORT)
    else:
        executor.start_polling(dispatcher,
                               skip_updates=True,
                               on_shutdown=on_polling_shutdown)
