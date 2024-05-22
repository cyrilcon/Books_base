from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    done_clear_back_cancel_keyboard,
    cancel_keyboard,
    demo_post_keyboard,
)
from tgbot.services import get_user_language, forming_text
from tgbot.states import AddBook

add_book_router_8 = Router()
add_book_router_8.message.filter(AdminFilter())


@add_book_router_8.callback_query(StateFilter(AddBook.select_price), F.data == "back")
async def back_to_add_book_7(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к добавлению файлов.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (AddBook).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    data = await state.get_data()
    files = data.get("files")
    formats = ", ".join(f"{file['format']}" for file in files)

    await call.message.edit_text(
        l10n.format_value(
            "add-book-files-send-more",
            {"formats": formats},
        ),
        reply_markup=done_clear_back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_files)


@add_book_router_8.callback_query(
    StateFilter(AddBook.select_price),
    F.data.in_({"85", "50", "do_not_publish", "not_from_a_user"}),
)
async def add_book_8(call: CallbackQuery, state: FSMContext):
    """
    Выбор цены.
    :param call: Нажатая кнопка.
    :param state: FSM (AddBook).
    :return: Сообщение для демо просмотра публикации и переход в FSM (preview).
    """

    button_pressed = call.data

    if button_pressed == "do_not_publish":
        await state.update_data(is_fasting=button_pressed)

    price = 50 if button_pressed == "50" else 85
    from_user = False if button_pressed == "not_from_a_user" else True
    await state.update_data(price=price)

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    data = await state.get_data()
    cover = data.get("cover")
    description = data.get("description")

    post_text = await forming_text(data, from_user=from_user, post=True)
    post_text_length = len(post_text)

    if post_text_length <= 1000:
        await call.message.delete()

        await call.message.answer_photo(
            cover,
            post_text,
            reply_markup=demo_post_keyboard(l10n),
        )
        await state.update_data(post_text=post_text)
        await state.set_state(AddBook.preview)
    else:
        await call.message.edit_text(
            l10n.format_value(
                "add-book-too-long-text",
                {
                    "description": description,
                    "post_text_length": post_text_length,
                },
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await state.set_state(AddBook.reduce_description)


@add_book_router_8.message(StateFilter(AddBook.reduce_description))
async def reduce_description(message: Message, bot: Bot, state: FSMContext):
    """
    Сокращение описания.
    :param message: Сообщение с ожидаемым сокращённым описанием.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для демо просмотра публикации и переход в FSM (preview).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    reduced_description = message.text
    await state.update_data(description=reduced_description)

    data = await state.get_data()
    cover = data.get("cover")

    post_text = await forming_text(data, post=True)
    post_text_length = len(post_text)

    if post_text_length <= 1000:
        await delete_keyboard(bot, message)

        await message.answer_photo(
            cover,
            post_text,
            reply_markup=demo_post_keyboard(l10n),
        )
        await state.update_data(post_text=post_text)
        await state.set_state(AddBook.preview)
    else:
        await message.answer(
            l10n.format_value(
                "add-book-too-long-text",
                {
                    "description": reduced_description,
                    "post_text_length": post_text_length,
                },
            ),
            reply_markup=cancel_keyboard(l10n),
        )
