from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import bold, text, link, italic

from settings import REPO_LINK, DEV_LINK

BOT_TITLE = emojize(text(*[
    "Hi there! Finding the right information in the ", italic("digital era"),
    " may be the real challenge nowadays because it's growing ", bold("exponentially"),
    " day by day! Whether you are a student preparing an essay or a researcher working ",
    "with the knowledge base, you spend a lot of time searching, filtering, and summarizing ",
    "text. ", link("Google", "https://www.google.com/"), " can assist you with the first two steps, "
    "but I will help with the last one!", " Send me a ", bold("plain text"), ", ", bold("file"),
    ", or ", bold("link to an external resource"), ", and I will summarize it for you in a word :grin:.\n\n",
    "I'm an open-source project, and you can find my ", link("source code here", REPO_LINK), ". ",
    "If you want to report an issue or have some suggestions for improvement, contact the ",
    link("maintainer", DEV_LINK), ".\n\n", "Choose the available options below:"
], sep=''))

SUMMARY_FROM_PLAIN_TEXT_OPTION = emojize(text(*['Plain text', ':notebook_with_decorative_cover:']))
SUMMARY_FROM_FILE_OPTION = emojize(text(*['File', ':floppy_disk:']))
SUMMARY_FROM_WEB_RESOURCE_OPTION = emojize(text(*['Web-resource', ':globe_with_meridians:']))
