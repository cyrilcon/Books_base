from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import find_user, create_user_link, ClearKeyboard
from tgbot.states import GivePremium

give_premium_router = Router()
give_premium_router.message.filter(AdminFilter())


@give_premium_router.message(Command("give_premium"))
async def give_premium(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Processing of the /give_premium command.
    :param message: /give_premium command.
    :param l10n: Language set by the user.
    :param state: FSM (GivePremium).
    :param storage: Storage for FSM.
    :return: Message to select the user and go to FSM (GivePremium).
    """

    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("give-premium-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GivePremium.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@give_premium_router.message(StateFilter(GivePremium.select_user), F.text)
async def give_premium_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    """
    Selects the user to issue Books_Base Premium status.
    :param message: A message with the expected username or user ID.
    :param l10n: Language set by the user.
    :param state: FSM (GivePremium).
    :param storage: Storage for FSM.
    :return: Issuing Books_Base Premium status to the user.
    """

    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(message.text, l10n)

    if user:
        id_user = user["id_user"]
        fullname = user["fullname"]
        username = user["username"]
        url_user = await create_user_link(fullname, username)

        response = await api.premium.create_premium(id_user)
        status = response.status

        if status == 201:
            await message.answer(
                l10n.format_value(
                    "give-premium-success",
                    {"url_user": url_user, "id_user": str(id_user)},
                )
            )
            await state.clear()
        else:
            sent_message = await message.answer(
                l10n.format_value(
                    "give-premium-error",
                    {"url_user": url_user, "id_user": str(id_user)},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                user_id=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
    else:
        sent_message = await message.answer(
            response_message, reply_markup=cancel_keyboard(l10n)
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            user_id=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
