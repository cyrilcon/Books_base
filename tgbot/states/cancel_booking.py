from aiogram.fsm.state import StatesGroup, State


class CancelBooking(StatesGroup):
    """Класс состояний для отмены заказа."""

    select_booking = State()
