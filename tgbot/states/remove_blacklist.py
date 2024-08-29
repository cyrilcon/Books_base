from aiogram.fsm.state import StatesGroup, State


class RemoveBlacklist(StatesGroup):
    """A class of states to remove a user from the blacklist."""

    select_user = State()
