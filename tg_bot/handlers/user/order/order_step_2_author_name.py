from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.api_client import api
from tg_bot.keyboards.inline import (
    cancel_keyboard,
    order_again_keyboard,
    serve_order_keyboard,
)
from tg_bot.services import (
    create_user_link,
    generate_id_order,
    get_fluent_localization,
    ClearKeyboard,
)
from tg_bot.states import Order

order_step_2_router = Router()


@order_step_2_router.callback_query(
    StateFilter(Order.author_name),
    F.data == "back",
)
async def back_to_order_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("order"),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Order.book_title)
    await call.answer()


@order_step_2_router.message(
    StateFilter(Order.author_name),
    F.text,
    flags={"safe_message": False},
)
async def order_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    id_user = message.from_user.id

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

    await api.orders.create_order(
        id_order=id_order,
        id_user=id_user,
        book_title=book_title,
        author_name=author_name,
    )

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

    user_link = create_user_link(
        full_name=message.from_user.full_name,
        username=message.from_user.username,
    )

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.order,
        text=l10n_chat.format_value(
            "order-success-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "book_title": book_title,
                "author_name": author_name,
                "id_order": str(id_order),
            },
        ),
        reply_markup=serve_order_keyboard(l10n_chat, id_order),
    )
