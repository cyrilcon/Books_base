from aiogram.fsm.state import StatesGroup, State


class ServeOrder(StatesGroup):
    """A class of states for order service."""

    select_order = State()
    select_book = State()
