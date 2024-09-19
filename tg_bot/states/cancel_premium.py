from aiogram.fsm.state import StatesGroup, State


class CancelPremium(StatesGroup):
    """A class of states to revoke Books_base Premium status."""

    select_user = State()
