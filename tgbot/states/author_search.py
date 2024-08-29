from aiogram.fsm.state import StatesGroup, State


class AuthorSearch(StatesGroup):
    """A class of states for author search"""

    select_author = State()
