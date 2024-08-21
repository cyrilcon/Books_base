from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
)
from tgbot.services import (
    ClearKeyboard,
    Messenger,
    get_user_language,
    generate_book_caption,
    is_book_article,
)
from tgbot.states import Serve

serve_router_2 = Router()
serve_router_2.message.filter(AdminFilter())


@serve_router_2.callback_query(StateFilter(Serve.send_book), F.data == "back")
async def back_to_serve_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("serve-select-booking"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Serve.select_booking)


@serve_router_2.message(StateFilter(Serve.send_book), F.text)
async def serve_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    if is_book_article(article):
        id_book = int(article.lstrip("#"))

        response = await api.books.get_book_by_id(id_book)
        status = response.status

        if status == 200:
            book = response.result

            data = await state.get_data()
            id_booking = data.get("id_booking")

            response = await api.orders.get_booking_by_id(id_booking)
            booking = response.result
            id_user_recipient = booking["id_user"]

            l10n_recipient = await get_user_language(id_user_recipient)

            is_sent = await Messenger.safe_send_message(
                bot=bot,
                user_id=id_user_recipient,
                text=l10n_recipient.format_value(
                    "serve-serviced",
                    {"id_booking": str(id_booking)},
                ),
            )

            if is_sent:
                caption = await generate_book_caption(data=book, l10n=l10n)

                await Messenger.safe_send_message(
                    bot=bot,
                    user_id=id_user_recipient,
                    text=caption,
                    photo=book["cover"],
                    # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
                )
                await message.answer(
                    l10n.format_value(
                        "serve-success",
                        {"id_booking": str(id_booking)},
                    )
                )
            else:
                await message.answer(l10n.format_value("error-user-blocked-bot"))

            await api.orders.delete_booking(id_booking)
            await state.clear()

        else:
            sent_message = await message.answer(
                l10n.format_value("article-not-found"),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                id_user=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
    else:
        sent_message = await message.answer(
            l10n.format_value("article-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
