from aiogram.fsm.state import StatesGroup, State


class GetProfile(StatesGroup):
    """A class of states for getting user profile."""

    select_user = State()
