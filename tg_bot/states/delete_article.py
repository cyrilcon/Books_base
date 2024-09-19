from aiogram.fsm.state import StatesGroup, State


class DeleteArticle(StatesGroup):
    """A class of states for deleting an article."""

    select_article = State()
