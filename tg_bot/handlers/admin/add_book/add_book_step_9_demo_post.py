from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.config import config
from tg_bot.keyboards.inline import deep_link_buy_keyboard
from tg_bot.states import AddBook

add_book_step_9_router = Router()


@add_book_step_9_router.callback_query(
    StateFilter(AddBook.preview),
    F.data == "post",
)
async def add_book_step_9(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    await call.message.edit_reply_markup()

    data = await state.get_data()
    is_post = data.get("is_post")
    id_book = data.get("id_book")
    cover = data.get("cover")
    book_caption = data.get("book_caption")

    await api.books.create_book(data=data)

    if is_post:
        deep_link_url = await create_start_link(bot, f"book_{id_book}")
        await bot.send_photo(
            chat_id=config.channel.books_base,
            photo=cover,
            caption=book_caption,
            reply_markup=deep_link_buy_keyboard(deep_link_url=deep_link_url),
        )
    await call.message.answer(l10n.format_value("add-book-success"))
    await state.clear()
    await call.answer()
