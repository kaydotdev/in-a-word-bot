import io
import re
import logging
import azure.functions as func

import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, ContentType
from aiogram.dispatcher import FSMContext

from datetime import datetime

from .static import *
from .processing import send_to_processing_queue
from .settings import MAX_FILE_SIZE, API_TOKEN
from .bot import bot_instance, dispatcher_instance, DialogFSM
from .utils import remove_html_tags, normalize_http_response,\
                   re_file_format, re_match_http_url


async def extract_summary(message: types.Message, state: FSMContext, text: str):
    async with state.proxy() as data:
        await send_to_processing_queue(message.chat.id, text, data['SUMMARY_TYPE'])

        await state.finish()
        await DialogFSM.main_menu.set()

        await message.answer(PROCESSING_STARTED, parse_mode=ParseMode.MARKDOWN,
                             disable_web_page_preview=True, reply_markup=main_menu_keyboard)


@dispatcher_instance.message_handler(commands=['cancel'], state='*')
async def handle_cancel(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_cancel")

    if await state.get_state() is None:
        return

    await state.finish()
    await DialogFSM.main_menu.set()
    await message.answer(COMMAND_CANCELLED, parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True, reply_markup=main_menu_keyboard)


@dispatcher_instance.message_handler(commands=['start'], state='*')
async def handle_start(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_start")

    if await state.get_state() is not None:
        await state.finish()

    await DialogFSM.main_menu.set()
    await message.answer(BOT_TITLE, parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True, reply_markup=main_menu_keyboard)


@dispatcher_instance.message_handler(lambda message: message.text in MAIN_MENU_OPTIONS, state=DialogFSM.main_menu)
async def handle_summary_content_assignment(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_summary_content_assignment")

    if message.text == MENU_NEW_SUMMARY_OPTION:
        await DialogFSM.content_type_selection.set()
        await message.answer(CHOOSE_AVAILABLE_OPTIONS, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=summary_content_option_keyboard)
    elif message.text == MENU_ABORT_REQUEST_OPTION:
        await message.answer("Request is aborted.", parse_mode=ParseMode.MARKDOWN)
    elif message.text == MENU_CHECK_STATUS_OPTION:
        await message.answer("Nothing to display.", parse_mode=ParseMode.MARKDOWN)
    elif message.text == MENU_ACKNOWLEDGEMENTS_OPTION:
        await message.answer(ACKNOWLEDGEMENTS, parse_mode=ParseMode.MARKDOWN)


@dispatcher_instance.message_handler(lambda message: message.text in SUMMARY_CONTENT_OPTIONS, state=DialogFSM.content_type_selection)
async def handle_summary_type_assignment(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_summary_type_assignment")

    async with state.proxy() as data:
        data['USER_DATA_TYPE'] = message.text

        await DialogFSM.summary_type_selection.set()
        await message.answer(SUMMARY_OPTION_TITLE, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=summary_type_option_keyboard)


@dispatcher_instance.message_handler(lambda message: message.text in SUMMARY_TYPE_OPTIONS, state=DialogFSM.summary_type_selection)
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


@dispatcher_instance.message_handler(state=DialogFSM.plain_text_processing, content_types=[ContentType.TEXT])
async def handle_plain_text_summary(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_plain_text_summary")

    await extract_summary(message, state, message.text)


@dispatcher_instance.message_handler(state=DialogFSM.file_processing, content_types=[ContentType.DOCUMENT])
async def handle_file_summary(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_file_summary")

    if message.document.file_size > MAX_FILE_SIZE:
        await message.answer(FILE_SIZE_EXCEEDED_LIMIT_ERROR, parse_mode=ParseMode.MARKDOWN)
    elif re.match(re_file_format, message.document.file_name) is None:
        await message.answer(FILE_WRONG_EXTENSION_ERROR, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer(PROCESSING_FILE, disable_web_page_preview=True, reply_markup=main_menu_keyboard)
        logging.info(f"[{datetime.now()}@{message.from_user.username}] processing file '{message.document.file_name}'")

        file: io.BytesIO = await bot_instance.download_file_by_id(message.document.file_id)
        file_containment = file.read().decode('utf-8')

        await extract_summary(message, state, file_containment)

        file.close()


@dispatcher_instance.message_handler(state=DialogFSM.web_resource_processing, content_types=[ContentType.TEXT])
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
            await DialogFSM.main_menu.set()
            await message.answer(WEB_CRAWLER_HTTP_ERROR,
                                    parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=main_menu_keyboard)


async def main(req: func.HttpRequest) -> func.HttpResponse:
    api_token = req.params.get('token', '')

    if api_token != API_TOKEN:
        return func.HttpResponse(status_code=403)

    Bot.set_current(bot_instance)
    Dispatcher.set_current(dispatcher_instance)

    request_update = types.Update(**req.get_json())
    await dispatcher_instance.process_updates([request_update])

    return func.HttpResponse(status_code=200)
