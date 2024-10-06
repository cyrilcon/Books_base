from aiogram.fsm.state import StatesGroup, State


class Saturday(StatesGroup):
    """A class of states for Saturday action."""

    select_book_1 = State()
    select_book_2 = State()
    select_book_3 = State()
