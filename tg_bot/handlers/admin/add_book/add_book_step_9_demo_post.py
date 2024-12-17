from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.api_client import api
from tg_bot.keyboards.inline import link_buy_keyboard
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
        link = await create_start_link(bot, f"book_{id_book}")
        await bot.send_photo(
            chat_id=config.channel.id,
            photo=cover,
            caption=book_caption,
            reply_markup=link_buy_keyboard(link=link),
        )
    await call.message.answer(l10n.format_value("add-book-success"))
    await state.clear()
    await call.answer()
