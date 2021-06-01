from aiogram.dispatcher.filters.state import State, StatesGroup


class DialogFSM(StatesGroup):
    main_menu = State()
