from aiogram.fsm.state import StatesGroup, State


class SendMessage(StatesGroup):
    """Класс состояний для отправки сообщения пользователю."""

    select_user = State()
    write_message = State()
