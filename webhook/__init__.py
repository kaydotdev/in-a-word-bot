import io
import logging
import azure.functions as func

import asyncio
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ContentType
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from datetime import datetime
from webhook.summary.abstract import *
from webhook.static_content import *
from webhook.summary.count import *
from webhook.settings import *
from webhook.states import *
from webhook.utils import *

loop = asyncio.get_event_loop()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, loop=loop)
dispatcher = Dispatcher(bot)
summary_transformer = SummaryTransformer(TOKENIZER_CONFIGS, TRANSFORMER_WEIGHTS_CONFIGS)


@dispatcher.message_handler(commands=['cancel'], state='*')
async def handle_cancel(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_cancel")
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.finish()
    await DialogFSM.main_menu.set()
    await message.answer(COMMAND_CANCELLED, parse_mode=ParseMode.MARKDOWN)
    await send_main_menu_keyboard(message)


@dispatcher.message_handler(commands=['start'], state='*')
async def handle_start(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_start")

    if await state.get_state() is not None:
        await state.finish()

    await DialogFSM.main_menu.set()
    await message.answer(BOT_TITLE, parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True)
    await send_main_menu_keyboard(message)


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
        await message.answer(GENERATING_SUMMARY, parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)
        generated_summary = await text_summary_async(message.text, data['SUMMARIZATION_CRITERIA_TYPE'])

        await state.finish()
        await DialogFSM.main_menu.set()

        # Max length of single Telegram message is 4096 characters. If gathered
        # text contains more symbols, it will be split into chunks of MAX_MESSAGE_LENGTH
        # and delivered in sequence
        for i in range(0, len(generated_summary), MAX_MESSAGE_LENGTH):
            await message.answer(generated_summary[i:i + MAX_MESSAGE_LENGTH],
                                 disable_web_page_preview=True)

        await send_main_menu_keyboard(message)


@dispatcher.message_handler(state=DialogFSM.file_processing, content_types=[ContentType.DOCUMENT])
async def handle_file_summary(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_file_summary")

    if message.document.file_size > MAX_FILE_SIZE:
        await message.answer(FILE_SIZE_EXCEEDED_LIMIT_ERROR, parse_mode=ParseMode.MARKDOWN)
    elif re.match(re_file_format, message.document.file_name) is None:
        await message.answer(FILE_WRONG_EXTENSION_ERROR, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer(PROCESSING_FILE, disable_web_page_preview=True, reply_markup=main_menu_keyboard)
        logging.info(f"[{datetime.now()}@{message.from_user.username}] processing file '{message.document.file_name}'")

        file: io.BytesIO = await bot.download_file_by_id(message.document.file_id)
        file_containment = file.read().decode('utf-8')

        async with state.proxy() as data:
            await message.answer(GENERATING_SUMMARY, parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)
            generated_summary = await text_summary_async(file_containment, data['SUMMARIZATION_CRITERIA_TYPE'])

            await state.finish()
            await DialogFSM.main_menu.set()

            for i in range(0, len(generated_summary), MAX_MESSAGE_LENGTH):
                await message.answer(generated_summary[i:i + MAX_MESSAGE_LENGTH],
                                     disable_web_page_preview=True)

        await send_main_menu_keyboard(message)
        file.close()


@dispatcher.message_handler(state=DialogFSM.web_resource_processing, content_types=[ContentType.TEXT])
async def handle_web_resource_summary(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_web_resource_summary")

    if re.match(re_match_http_url, message.text) is None:
        await message.answer(INCORRECT_HTTP_FORMAT_ERROR, parse_mode=ParseMode.MARKDOWN)
    else:
        async with state.proxy() as data:
            try:
                await message.answer(SENDING_REQUEST, parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)

                async with aiohttp.ClientSession() as session:
                    async with session.get(message.text) as response:
                        response_body = await response.text()

                await message.answer(GENERATING_SUMMARY, parse_mode=ParseMode.MARKDOWN, reply_markup=empty_keyboard)
                generated_summary = await text_summary_async(remove_html_tags(response_body),
                                                             data['SUMMARIZATION_CRITERIA_TYPE'])

                await state.finish()
                await DialogFSM.main_menu.set()

                for i in range(0, len(generated_summary), MAX_MESSAGE_LENGTH):
                    await message.answer(generated_summary[i:i + MAX_MESSAGE_LENGTH],
                                         disable_web_page_preview=True)

                await send_main_menu_keyboard(message)
            except Exception as ex:
                logging.error(f"[{datetime.now()}@bot] Failed to parse web resource content: {ex}")

                await state.finish()
                await DialogFSM.main_menu.set()
                await message.answer(WEB_CRAWLER_HTTP_ERROR,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=main_menu_keyboard)


async def text_summary_async(entry_text: str, criteria: str):
    if criteria == SUMMARIZE_BY_FREQUENCY_OPTION:
        return tf_idf_summary(entry_text)
    elif criteria == SUMMARIZE_BY_ABSTRACTION_OPTION:
        return summary_transformer.summarize(entry_text)
    else:
        return NO_SUMMARIZATION_CRITERIA_ERROR


async def send_main_menu_keyboard(message: types.Message):
    await message.answer(CHOOSE_AVAILABLE_OPTIONS, parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True, reply_markup=main_menu_keyboard)


async def main(req: func.HttpRequest) -> func.HttpResponse:
    Bot.set_current(bot)

    dispatcher.storage = MemoryStorage()
    request_update = types.Update(**req.get_json())

    await dispatcher.process_updates([request_update])
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

    return func.HttpResponse(status_code=200)
