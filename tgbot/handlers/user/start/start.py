import re

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.services import get_fluent_localization, safe_send_message, forming_text

start_router = Router()


@start_router.message(CommandStart())
@start_router.message(
    CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r"book_(\d+)")))
)
async def start(
    message: Message,
    bot: Bot,
    state: FSMContext,
    command: CommandObject,
    config: Config,
):
    """
    Обработка команды /start.
    :param message: Команда /start.
    :param bot: Экземпляр бота.
    :param state: Любое FSM состояние для аварийного сброса.
    :param command: Встроенная команда на получение книги по артикулу.
    :param config: Config с параметрами бота.
    :return: Приветственное сообщение бота | Найденная книга.
    """

    await state.clear()

    id_user = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username

    response = await api.users.get_user(id_user)
    status = response.status
    user = response.result

    if status == 200:
        language = user["language"]
        await api.users.update_user(id_user, fullname=fullname, username=username)
    else:
        language = message.from_user.language_code
        await api.users.add_user(id_user, language, fullname, username)

    l10n = get_fluent_localization(language)
    text = f", <b>{fullname}</b>" if fullname else None

    if command.args is not None:
        article = command.args.split("_")[1]

        response = await api.books.get_book(article)
        status = response.status
        book = response.result

        if status == 200:
            post_text = await forming_text(book, l10n)

            await safe_send_message(
                config=config,
                bot=bot,
                id_user=id_user,
                text=post_text,
                photo=book["cover"],
                # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
            )

        else:
            await message.answer(
                l10n.format_value(
                    "search-book-does-not-exist",
                    {"article": "#{:04d}".format(int(article))},
                )
            )
    else:
        await message.answer(l10n.format_value("start-text", {"additional_text": text}))
