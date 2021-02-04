import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import bold, text
from settings import API_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)


DISCLAIMER = emojize(text(*[
    ":mag:", "Greetings, I am", bold("'A GRAM OF WORD'"), "bot",
    "an open Telegram bot that", bold("collects and aggregates"),
    "scientific lectures and articles from the known sources",
    "using meta-searching algorithms and text analysis algorithms.",
    "The result of the aggregation process is a brief text summary",
    "of collected resources.", "Full list of the available commands:\n\n",
    "/list - print known resource list\n",
    "/query - collect a resource summary by user's topic"
], sep=' '))


@dispatcher.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    await message.answer(DISCLAIMER, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
