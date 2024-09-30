import re

from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import buy_or_read_keyboard
from tg_bot.services import ClearKeyboard, BookFormatter, generate_book_caption

start_router = Router()


@start_router.message(
    CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r"book_(\d+)")))
)
async def start_deep_link(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    command: CommandObject,
):
    await ClearKeyboard.clear(message, storage)
    await state.clear()

    id_book = int(command.args.split("_")[1])

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        article = BookFormatter.format_article(id_book=id_book)

        await message.answer(
            l10n.format_value(
                "error-book-unavailable",
                {"article": article},
            )
        )
        return

    book = response.get_model()
    id_user = message.from_user.id

    caption = await generate_book_caption(
        book_data=book,
        l10n=l10n,
        id_user=id_user,
    )

    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=await buy_or_read_keyboard(
            l10n=l10n,
            id_book=id_book,
            id_user=id_user,
        ),
    )


@start_router.message(CommandStart())
async def start(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)
    await state.clear()

    full_name = message.from_user.full_name
    await message.answer(
        l10n.format_value(
            "start",
            {"full_name": full_name},
        )
    )
