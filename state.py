from aiogram.dispatcher.filters.state import State, StatesGroup


class QueryStateMachine(StatesGroup):
    awaiting_user_topic = State()
    awaiting_sources_list_option = State()
