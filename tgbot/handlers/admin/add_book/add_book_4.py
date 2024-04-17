from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import back_and_cancel_buttons
from tgbot.services import get_user_language
from tgbot.states import AddBook

add_book_router_4 = Router()
add_book_router_4.message.filter(AdminFilter())


@add_book_router_4.callback_query(
    StateFilter(AddBook.add_description), F.data == "BACK_and_cancel"
)
async def back_to_add_book_3(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к добавлению автора(ов).
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (AddBook).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-authors"),
        reply_markup=back_and_cancel_buttons,
    )
    await state.set_state(AddBook.add_authors)


@add_book_router_4.message(StateFilter(AddBook.add_description))
async def add_book_4(message: Message, bot: Bot, state: FSMContext):
    """
    Добавление описания.
    :param message: Сообщение с ожидаемым описанием.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для добавления жанров и переход в FSM (add_genres).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    description = message.text

    if len(description) > 850:
        await message.answer(
            l10n.format_value("add-book-description-too-long"),
            reply_markup=back_and_cancel_buttons,
        )
    else:
        await message.answer(
            l10n.format_value("add-book-genres"),
            reply_markup=back_and_cancel_buttons,
        )
        await state.update_data(description=description)
        await state.set_state(AddBook.add_genres)
