from aiogram.dispatcher.filters.state import State, StatesGroup


class DialogFSM(StatesGroup):
    main_menu = State()
    summarization_criteria = State()

    plain_text_processing = State()
    file_processing = State()
    web_resource_processing = State()
