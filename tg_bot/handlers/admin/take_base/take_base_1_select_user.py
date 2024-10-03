from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import find_user, ClearKeyboard, create_user_link
from tg_bot.states import TakeBase

take_base_step_1_router = Router()


@take_base_step_1_router.message(Command("take_base"))
async def take_base(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("take-base-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(TakeBase.select_user)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@take_base_step_1_router.message(
    StateFilter(TakeBase.select_user),
    F.text,
)
async def take_base_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    user, response_message = await find_user(l10n, message.text)

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
    user_link = create_user_link(user.full_name, user.username)

    sent_message = await message.answer(
        l10n.format_value(
            "take-base-deduct-base",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "base_balance": user.base_balance,
            },
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(id_user_recipient=id_user, user_link=user_link)
    await state.set_state(TakeBase.deduct_base)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
