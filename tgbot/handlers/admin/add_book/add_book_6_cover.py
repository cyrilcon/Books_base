from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    back_and_cancel_keyboard,
    ready_clear_back_cancel_keyboard,
)
from tgbot.services import get_user_language
from tgbot.states import AddBook

add_book_router_6 = Router()
add_book_router_6.message.filter(AdminFilter())


@add_book_router_6.callback_query(StateFilter(AddBook.add_cover), F.data == "back")
async def back_to_add_book_5(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к добавлению жанров.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (AddBook).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    data = await state.get_data()
    genres = data.get("genres")
    ready_made_genres = " ".join(["#" + genre["genre"] for genre in genres])

    await call.message.edit_text(
        l10n.format_value(
            "add-book-genres-example",
            {"ready_made_genres": ready_made_genres},
        ),
        reply_markup=ready_clear_back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_genres)


@add_book_router_6.message(StateFilter(AddBook.add_cover), F.photo)
async def add_book_6(message: Message, bot: Bot, state: FSMContext):
    """
    Добавление обложки.
    :param message: Сообщение с ожидаемой фотографией обложки.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для добавления обложки и переход в FSM (add_files).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    cover = message.photo[-1].file_id

    await message.answer(
        l10n.format_value("add-book-files"),
        reply_markup=back_and_cancel_keyboard(l10n),
    )

    await state.update_data(cover=cover)
    await state.set_state(AddBook.add_files)
