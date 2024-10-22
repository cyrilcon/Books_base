from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from api.books_base_api.schemas import UserSchema
from tg_bot.keyboards.inline import my_books_keyboard
from tg_bot.services import generate_book_caption

my_books_page_router = Router()


@my_books_page_router.callback_query(
    F.data.startswith("my_books_page"),
    flags={"safe_message": False},
)
async def my_books_page(
    call: CallbackQuery,
    l10n: FluentLocalization,
    user: UserSchema,
):
    if user.is_premium:
        await call.message.edit_reply_markup()
        await call.answer(
            l10n.format_value("my-books-user-has-premium-alert"),
            show_alert=True,
        )
        return

    page = int(call.data.split(":")[-1])

    response = await api.users.get_book_ids(id_user=user.id_user)
    book_ids = response.result

    response = await api.books.get_book_by_id(id_book=book_ids[page - 1])
    book = response.get_model()

    caption = await generate_book_caption(
        book_data=book,
        l10n=l10n,
        user=user,
    )
    await call.message.edit_media(
        media=InputMediaPhoto(media=book.cover, caption=caption),
        reply_markup=my_books_keyboard(
            l10n=l10n,
            book_ids=book_ids,
            page=page,
        ),
    )
    await call.answer()
