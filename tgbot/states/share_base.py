from aiogram.fsm.state import StatesGroup, State


class ShareBase(StatesGroup):
    """A class of states for sending base to the user."""

    select_user = State()
