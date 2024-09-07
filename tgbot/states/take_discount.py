from aiogram.fsm.state import StatesGroup, State


class TakeDiscount(StatesGroup):
    """A class of states for taking a discount."""

    select_user = State()
