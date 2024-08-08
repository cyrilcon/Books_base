from aiogram.fsm.state import StatesGroup, State


class GiveBase(StatesGroup):
    """A class of states for giving out the base."""

    select_user = State()
    send_base = State()
