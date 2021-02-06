import re
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import bold, text, link
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import *
from sources import KNOWN_SOURCES
from state import *


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
cache_storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=cache_storage)


DISCLAIMER = emojize(text(*[
    ":mag:", "Greetings, I am", bold("'A GRAM OF WORD'"), "bot,",
    "an open Telegram bot that", bold("collects and aggregates"),
    "scientific lectures and articles from the known sources",
    "using meta-searching algorithms and text analysis algorithms.",
    "The result of the aggregation process is a brief text summary",
    "of collected resources.", "Full list of the available commands:\n\n",
    "/list - print known resource list\n",
    "/query - collect a resource summary by user's topic\n\n",
    link("Source code", REPO_LINK), link("Developer", DEV_LINK)
], sep=' '))


@dispatcher.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    await message.answer(DISCLAIMER, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@dispatcher.message_handler(commands=['list'])
async def handle_list(message: types.Message):
    sources_list = text(*[text(link(source['name'], source['url']), "-", source['description'], sep=' ')
                          for source in KNOWN_SOURCES], sep='\n')
    await message.answer(sources_list, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@dispatcher.message_handler(commands=['query'])
async def handle_query(message: types.Message):
    await QueryStateMachine.awaiting_user_topic.set()
    response = text(*["Send me your topic, it should contain",
                      bold("only Latin letters"),
                      "and be not longer than",
                      bold("50 characters")], sep=' ')
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)


@dispatcher.message_handler(lambda message: message.text.isascii(), state=QueryStateMachine.awaiting_user_topic)
async def handle_query_awaiting_user_topic(message: types.Message, state: FSMContext):
    if len(re.findall(r'^[a-zA-Z0-9\s]{1,50}$', message.text)) == 0:
        await message.answer("User topic doesn't follow requirements above. Try again.")
    else:
        async with state.proxy() as data:
            data['user_topic'] = message.text

        await QueryStateMachine.next()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Yes", "No")

        await message.answer("List used resources after summary?", reply_markup=markup)


@dispatcher.message_handler(lambda message: message.text in ["Yes", "No"],
                            state=QueryStateMachine.awaiting_sources_list_option)
async def handle_query_awaiting_awaiting_sources_list_option(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sources_list'] = message.text
        await message.answer("Processing the request...", reply_markup=types.ReplyKeyboardRemove())

        # TODO: Place meta-search algorithm here
        # ...

        response = text(*["User topic:",
                          bold(data['user_topic']),
                          "Sources list option:",
                          bold(data['sources_list'])], sep=' ')

        await message.answer(response, parse_mode=ParseMode.MARKDOWN)

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
