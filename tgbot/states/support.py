from aiogram.fsm.state import StatesGroup, State


class Support(StatesGroup):
    """A class of states for tech support."""

    reply_to_admin = State()
    reply_to_user = State()
