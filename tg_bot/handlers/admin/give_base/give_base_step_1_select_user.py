from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import find_user, ClearKeyboard, create_user_link
from tg_bot.states import GiveBase

give_base_step_1_router = Router()


@give_base_step_1_router.message(Command("give_base"))
async def give_base_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("give-base-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveBase.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@give_base_step_1_router.message(StateFilter(GiveBase.select_user), F.text)
async def give_base_1_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(message.text, l10n)

    if not user:
        sent_message = await message.answer(
            response_message, reply_markup=cancel_keyboard(l10n)
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_user = user.id_user
    full_name = user.full_name
    username = user.username
    user_link = await create_user_link(full_name, username)

    sent_message = await message.answer(
        l10n.format_value(
            "give-base-prompt-transfer",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "base_balance": user.base_balance,
            },
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(id_user_recipient=id_user, user_link=user_link)
    await state.set_state(GiveBase.transfer)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
