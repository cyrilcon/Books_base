from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
    support_answer_keyboard,
)
from tgbot.services import (
    get_user_language,
    safe_send_message,
    get_url_user,
)
from tgbot.states import Support

support_router = Router()


@support_router.message(Command("support"))
async def support(message: Message, state: FSMContext):
    """
    Обработка команды /support.
    :param message: Команда /support.
    :param state: FSM (Support).
    :return: Сообщение для написания названия книги и переход в FSM (message_to_admin).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("support"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(Support.message_to_admin)


@support_router.message(StateFilter(Support.message_to_admin))
async def support_process(
    message: Message, bot: Bot, state: FSMContext, config: Config
):
    """
    Отправка сообщения в чат тех-поддержки.
    :param message: Сообщение с ожидаемым сообщением пользователя.
    :param bot: Экземпляр бота.
    :param state: FSM (Support).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешной отправке сообщения в тех-поддержку.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username
    l10n = await get_user_language(id_user)

    url_user = await get_url_user(fullname, username)

    await bot.forward_message(
        chat_id=config.tg_bot.support_chat,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )

    await safe_send_message(
        config=config,
        bot=bot,
        id_user=config.tg_bot.support_chat,
        text=l10n.format_value(
            "support-to-admin", {"url_user": url_user, "id_user": str(id_user)}
        ),
        reply_markup=support_answer_keyboard(l10n, id_user),
    )
    await message.answer(l10n.format_value("support-message-sent"))
    await state.clear()


@support_router.callback_query(F.data == "support_reply_to_admin")
async def support_reply_to_admin(call: CallbackQuery, state: FSMContext):
    """
    Отправка ответа адимину.
    :param call: Кнопка "Ответить".
    :param state: FSM (Support).
    :return: Сообщение об успешной отправке сообщения пользователю.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    await call.message.answer(
        l10n.format_value("support-message-sent-to-admin"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Support.message_to_admin)
