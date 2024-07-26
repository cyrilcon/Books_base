from aiogram.fsm.state import StatesGroup, State


class GivePremium(StatesGroup):
    """A class of states for the issuance of Books_base Premium status."""

    select_user = State()
