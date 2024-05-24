from aiogram.fsm.state import StatesGroup, State


class Booking(StatesGroup):
    """Класс состояний для заказа книги."""

    send_title = State()
    send_author = State()
