from aiogram.fsm.state import StatesGroup, State


class TakeBase(StatesGroup):
    """A class of states for taking away the base."""

    select_user = State()
    deduct_base = State()
