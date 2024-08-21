from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.config import config
from tgbot.keyboards.inline import (
    cancel_keyboard,
    order_again_keyboard,
    serve_keyboard,
)
from tgbot.services import (
    ClearKeyboard,
    create_user_link,
    get_user_language,
    generate_id_order,
)
from tgbot.states import Order

order_step_2_router = Router()


@order_step_2_router.callback_query(StateFilter(Order.author_name), F.data == "back")
async def back_to_order_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("order-step-1-book-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Order.book_title)
    await call.answer()


@order_step_2_router.message(StateFilter(Order.author_name))
async def order_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    id_user = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    author_name = message.text

    if len(author_name) > 255:
        sent_message = await message.answer(
            l10n.format_value("order-error-author-name-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_order = generate_id_order(id_user)

    data = await state.get_data()
    book_title = data["book_title"]

    await api.orders.create_order(id_order, id_user, book_title, author_name)

    await message.answer(
        l10n.format_value(
            "order-success",
            {
                "book_title": book_title,
                "author_name": author_name,
                "id_order": str(id_order),
            },
        ),
        reply_markup=order_again_keyboard(l10n),
    )
    await state.clear()

    user_link = await create_user_link(full_name, username)
    language_code = await get_user_language(config.tg_bot.super_admin)

    await bot.send_message(
        chat_id=config.tg_bot.booking_chat,
        text=l10n.format_value(
            "order-received-from-user",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "book_title": book_title,
                "author_name": author_name,
                "id_order": str(id_order),
            },
        ),
        reply_markup=serve_keyboard(language_code, id_order),
    )
