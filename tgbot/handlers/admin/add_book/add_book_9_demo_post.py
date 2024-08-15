from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.config import config
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import deep_link_buy_keyboard
from tgbot.services import Messenger
from tgbot.states import AddBook

add_book_router_9 = Router()
add_book_router_9.message.filter(AdminFilter())


@add_book_router_9.callback_query(StateFilter(AddBook.preview), F.data == "post")
async def add_book_9(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    await call.answer(cache_time=1)

    data = await state.get_data()
    id_book = data.get("id_book")
    caption = data.get("caption")
    cover = data.get("cover")
    post = data.get("post")

    await api.books.create_book(data)

    deep_link = await create_start_link(bot, f"book_{id_book}")

    if post:
        await Messenger.safe_send_message(
            bot=bot,
            user_id=config.tg_bot.tg_channel,
            text=caption,
            photo=cover,
            reply_markup=deep_link_buy_keyboard(deep_link),
        )

    await state.clear()
    await call.message.edit_reply_markup()
    await call.message.answer(l10n.format_value("add-book-success"))
