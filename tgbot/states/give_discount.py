from aiogram.fsm.state import StatesGroup, State


class GiveDiscount(StatesGroup):
    """A class of states for giving a discount."""

    select_user = State()
    select_discount = State()
