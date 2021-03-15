import re
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import bold, text, link
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from datetime import datetime

from processing import *
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

WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"


@dispatcher.message_handler(commands=['cancel'], state='*')
async def handle_cancel(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_cancel")
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.finish()
    await message.answer('Operation cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dispatcher.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_start")
    await message.answer(DISCLAIMER, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@dispatcher.message_handler(commands=['list'])
async def handle_list(message: types.Message):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_list")
    sources_list = text(*[text(link(source['name'], source['url']), "-", source['description'], sep=' ')
                          for source in KNOWN_SOURCES], sep='\n')
    await message.answer(sources_list, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@dispatcher.message_handler(commands=['query'])
async def handle_query(message: types.Message):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_query")
    await QueryStateMachine.awaiting_user_topic.set()
    response = text(*["Send me your topic, it should contain",
                      bold("only Latin letters"),
                      "and be not longer than",
                      bold("50 characters"), "."], sep=' ')
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)


@dispatcher.message_handler(lambda message: message.text.isascii(), state=QueryStateMachine.awaiting_user_topic)
async def handle_query_awaiting_user_topic(message: types.Message, state: FSMContext):
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_query_awaiting_user_topic")
    if len(re.findall(r'^[a-zA-Z0-9\s]{1,50}$', message.text)) == 0:
        logging.warning(f"[{datetime.now()}@{message.from_user.username}] handle_query_awaiting_user_topic invalid "
                        f"user topic")
        await message.reply("User topic doesn't follow requirements above. Try again.")
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
    logging.info(f"[{datetime.now()}@{message.from_user.username}] handle_query_awaiting_awaiting_sources_list_option")
    async with state.proxy() as data:
        data['sources_list'] = message.text
        await message.answer(emojize(text(*[":mag:", "Collecting resources..."], sep=' ')),
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=types.ReplyKeyboardRemove())

        try:
            resources = await collect_ranked_hrefs(data['user_topic'], MAX_SOURCE_POOL)
            resources_list = "\n\nUsed resources:\n\n" + text(*[text(link(resource[0], resource[1]))
                                                                for resource in resources], sep='\n')

            await message.answer(resources_list, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        except Exception as ex:
            logging.error(f"[{datetime.now()}@{message.from_user.username}] Error: {ex}")
            await message.answer(emojize(text(*["No resource found on desirable topic", ":disappointed:"], sep=' ')),
                                 parse_mode=ParseMode.MARKDOWN)

    await state.finish()


async def on_startup(_dispatcher):
    logging.warning(f'[{datetime.now()}@root] setting web hook')
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(_dispatcher):
    logging.warning(f'[{datetime.now()}@root] deleting web hook')

    await bot.delete_webhook()

    logging.warning(f'[{datetime.now()}@root] shutting down bot')
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

    logging.warning(f'[{datetime.now()}@root] bot was successfully shut down')


if __name__ == '__main__':
    if WEBHOOK_ENABLED is True:
        executor.start_webhook(dispatcher,
                               WEBHOOK_PATH,
                               on_startup=on_startup,
                               on_shutdown=on_shutdown,
                               skip_updates=True,
                               host=WEBHOOK_IP,
                               port=WEBHOOK_PORT)
    else:
        executor.start_polling(dispatcher,
                               skip_updates=True)
