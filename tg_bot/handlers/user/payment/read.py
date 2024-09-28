from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from services import send_files
from api.books_base_api import api

read_router = Router()


@read_router.callback_query(F.data.startswith("read"))
async def read(
    call: CallbackQuery,
    l10n: FluentLocalization,
    bot: Bot,
):
    id_book = int(call.data.split(":")[-1])

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        await call.message.edit_reply_markup()
        await call.message.answer(
            l10n.format_value(
                "error-book-unavailable",
                {"id_book": id_book},
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
