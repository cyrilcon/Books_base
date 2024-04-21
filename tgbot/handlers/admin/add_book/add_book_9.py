from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.config import Config
from tgbot.filters import AdminFilter
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
    cover = data.get("cover")
    price = data.get("price")

    # Добавить книгу в бд

    if price != "do_not_publish":
        await send_message(
            config=config,
            bot=bot,
            user_id=config.tg_bot.channel,
            text=call.message.caption,
            photo=cover,
        )

    await state.clear()
    await call.message.edit_reply_markup()
    await call.message.answer(l10n.format_value("add-book-complete"))
