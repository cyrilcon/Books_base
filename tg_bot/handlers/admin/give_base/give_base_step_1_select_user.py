from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import find_user, create_user_link
from tg_bot.states import GiveBase

give_base_step_1_router = Router()


@give_base_step_1_router.message(
    StateFilter(GiveBase.select_user),
    F.text,
)
async def give_base_1_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    user, response_message = await find_user(l10n, message.text)

    if not user:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
        return

    id_user = user.id_user
    user_link = create_user_link(user.full_name, user.username)

    await message.answer(
        l10n.format_value(
            "give-base-transfer-base",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "base_balance": user.base_balance,
            },
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(id_user_recipient=id_user, user_link=user_link)
    await state.set_state(GiveBase.transfer_base)
