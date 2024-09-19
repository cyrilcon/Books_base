from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from fluent.runtime import FluentLocalization

from tg_bot.api.books_base_api import api
from tg_bot.config import config
from tg_bot.keyboards.inline import deep_link_buy_keyboard
from tg_bot.states import AddBook

add_book_step_9_router = Router()


@add_book_step_9_router.callback_query(StateFilter(AddBook.preview), F.data == "post")
async def add_book_step_9(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    data = await state.get_data()
    id_book = data.get("id_book")
    caption = data.get("caption")
    cover = data.get("cover")
    is_post = data.get("is_post")

    await api.books.create_book(data)

    if is_post:
        deep_link = await create_start_link(bot, f"book_{id_book}")
        await bot.send_photo(
            chat_id=config.channel.books_base,
            photo=cover,
            caption=caption,
            reply_markup=deep_link_buy_keyboard(deep_link),
        )
    await state.clear()
    await call.message.edit_reply_markup()
    await call.message.answer(l10n.format_value("add-book-success"))
    await call.answer()
