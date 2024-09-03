from aiogram.fsm.state import StatesGroup, State


class AddArticle(StatesGroup):
    """A class of states for adding an article."""

    add_title = State()
    add_link = State()
    select_language_code = State()
