import re

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LinkPreviewOptions

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.keyboards.inline import (
    cancel_keyboard,
)
from tgbot.services import (
    get_user_language,
    send_message,
)
from tgbot.states import ShareBase

share_base_router_2 = Router()


@share_base_router_2.callback_query(F.data == "share_base_back_to_select_user")
async def back_to_share_base_1(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к выбору пользователя.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (ShareBase).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("share-base-select-user"),
        reply_markup=cancel_keyboard(l10n),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await state.set_state(ShareBase.select_user)


@share_base_router_2.callback_query(F.data.startswith("share_base"))
async def share_base_2(call: CallbackQuery, bot: Bot, config: Config):
    """
    Указывается количество base, чтобы отправить их выбранному пользователю.
    :param call: Нажатая кнопка с выбранным количеством base.
    :param bot: Экземпляр бота.
    :param config: Config с параметрами бота.
    :return: Сообщение об успешной отправке base выбранному пользователю.
    """

    id_user = call.from_user.id
    username = call.from_user.username
    l10n = await get_user_language(id_user)

    if username:
        bases = int(call.data.split(":")[-1])

        pattern = r"@([a-zA-Z](?!_)(?!.*?_{2})\w{2,30}[a-zA-Z0-9])"
        username_recipient = re.search(pattern, call.message.text).group(1)

        response = await api.users.get_user_by_username(username_recipient)
        user_recipient = response.result

        response = await api.users.get_user(id_user)
        user_sender = response.result
        user_sender_account = user_sender["base"]
        residue = user_sender_account - bases

        if residue >= 0:
            await call.answer(cache_time=1)

            id_user_recipient = user_recipient["id_user"]
            l10n_recipient = await get_user_language(id_user_recipient)

            amount_base = l10n_recipient.format_value(
                "base-store-account-amount-base",
                {"bases": user_recipient["base"] + bases},
            )

            is_sent = await send_message(
                config=config,
                bot=bot,
                id_user=id_user_recipient,
                text=l10n_recipient.format_value(
                    "share-base-came-in",
                    {
                        "bases": bases,
                        "username": user_sender["username"],
                        "amount_base": amount_base,
                    },
                ),
            )
            if is_sent:
                await api.users.update_user(
                    id_user=user_sender["id_user"],
                    base=residue,
                )
                await api.users.update_user(
                    id_user=id_user_recipient,
                    base=user_recipient["base"] + bases,
                )

                amount_base = l10n.format_value(
                    "base-store-account-amount-base",
                    {"bases": residue},
                )

                await call.message.edit_text(
                    l10n.format_value(
                        "share-base-was-sent",
                        {
                            "bases": bases,
                            "username": user_recipient,
                            "amount_base": amount_base,
                        },
                    ),
                )
            else:
                await call.answer(
                    l10n.format_value("share-base-error"),
                    show_alert=True,
                )
        else:
            await call.answer(
                l10n.format_value(
                    "share-base-not-enough-base", {"username": username_recipient}
                ),
                show_alert=True,
            )
    else:
        await call.answer(
            l10n.format_value("share-base-sender-does-not-have-username"),
            show_alert=True,
        )
