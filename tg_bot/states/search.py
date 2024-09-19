from aiogram.fsm.state import StatesGroup, State


class Search(StatesGroup):
    """A class of states for search"""

    by_author = State()
    by_genre = State()
