from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.config import config
from tg_bot.services import (
    send_files,
    ClearKeyboard,
    BookFormatter,
    get_fluent_localization,
    create_user_link,
)

read_router = Router()


@read_router.callback_query(F.data.startswith("read"))
async def read(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(call, storage)
    await state.clear()

    id_book = int(call.data.split(":")[-1])

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        await call.message.edit_reply_markup()

        article = BookFormatter.format_article(id_book=id_book)

        await call.message.answer(
            l10n.format_value(
                "error-book-unavailable",
                {"article": article},
            )
        )
        await call.answer()
        return

    book = response.get_model()

    await send_files(
        bot=bot,
        chat_id=call.from_user.id,
        caption=book.title,
        files=book.files,
    )
    await call.answer()

    id_user = call.from_user.id

    response = await api.users.get_user_by_id(id_user=id_user)
    user = response.get_model()

    if user.is_premium:
        user_link = await create_user_link(user.full_name, user.username)
        article = BookFormatter.format_article(id_book=id_book)

        l10n_chat = get_fluent_localization(config.chat.language_code)
        await bot.send_message(
            chat_id=config.chat.payment,
            text=l10n_chat.format_value(
                "read",
                {
                    "user_link": user_link,
                    "id_user": str(id_user),
                    "title": book.title,
                    "article": article,
                },
            ),
        )
