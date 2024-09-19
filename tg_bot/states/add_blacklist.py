from aiogram.fsm.state import StatesGroup, State


class AddBlacklist(StatesGroup):
    """A class of states for adding a user to the blacklist."""

    select_user = State()
