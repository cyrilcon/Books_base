from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import deep_link_buy_keyboard
from tgbot.services import get_user_language, send_message
from tgbot.states import AddBook

add_book_router_9 = Router()
add_book_router_9.message.filter(AdminFilter())


@add_book_router_9.callback_query(StateFilter(AddBook.preview), F.data == "post")
async def add_book_9(call: CallbackQuery, bot: Bot, state: FSMContext, config: Config):
    """
    Добавление книги в бд, публикация поста в канале.
    :param call: Нажатая кнопка "Опубликовать".
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :param config: Config с параметрами бота.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    data = await state.get_data()
    id_book = data.get("id_book")
    cover = data.get("cover")
    price = data.get("price")
    post_text = data.get("post_text")

    await api.books.add_book(data)

    deep_link = await create_start_link(bot, f"book_{id_book}")

    if price != "do_not_publish":
        await send_message(
            config=config,
            bot=bot,
            id_user=config.tg_bot.channel,
            text=post_text,
            photo=cover,
            reply_markup=deep_link_buy_keyboard(deep_link),
        )

    await state.clear()
    await call.message.edit_reply_markup()
    await call.message.answer(l10n.format_value("add-book-complete"))
