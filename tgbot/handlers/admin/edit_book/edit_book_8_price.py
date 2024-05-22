from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    edit_keyboard,
    prices_keyboard,
)
from tgbot.services import get_user_language, forming_text, send_message

edit_book_8_price_router = Router()
edit_book_8_price_router.message.filter(AdminFilter())


@edit_book_8_price_router.callback_query(F.data.startswith("edit_price"))
async def edit_price(call: CallbackQuery):
    """
    Обработка кнопки "Цена".
    :param call: Кнопка "Цена".
    :return: Сообщение для изменения цены книги.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book(id_book)
    book = response.result

    await call.message.answer(
        l10n.format_value("edit-book-price"),
        reply_markup=prices_keyboard(id_book),
    )


@edit_book_8_price_router.callback_query(F.data.startswith("update_price"))
async def update_price(call: CallbackQuery, bot: Bot, config: Config):
    """
    Обработка кнопки "85₽" или "85₽".
    :param call: Кнопка "85₽" или "85₽".
    :param bot: Экземпляр бота.
    :param config: Config с параметрами бота.
    :return: Сообщение об успешном изменении цены.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    id_edit_book = int(call.data.split(":")[-1])
    price = int(call.data.split(":")[-2])

    response = await api.books.update_book(id_edit_book, price=price)
    status = response.status
    book = response.result

    if status == 200:
        post_text = await forming_text(book, l10n)

        await call.message.edit_text(
            l10n.format_value("edit-book-successfully-changed")
        )
        await send_message(
            config=config,
            bot=bot,
            id_user=id_user,
            text=post_text,
            photo=book["cover"],
            reply_markup=edit_keyboard(l10n, book["id_book"]),
        )
