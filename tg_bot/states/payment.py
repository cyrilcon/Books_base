from aiogram.fsm.state import StatesGroup, State


class Payment(StatesGroup):
    """A class of states for payment."""

    premium = State()
    book = State()
