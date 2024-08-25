from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import cancel_keyboard, edit_book_keyboard
from tgbot.services import ClearKeyboard, generate_book_caption
from tgbot.states import EditBook

edit_description_router = Router()


@edit_description_router.callback_query(F.data.startswith("edit_description"))
async def edit_description(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book)
    book = response.get_model()

    sent_message = await call.message.answer(
        l10n.format_value(
            "edit-book-prompt-description",
            {"description": f"<code>{book.description}</code>"},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_description)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@edit_description_router.message(StateFilter(EditBook.edit_description), F.text)
async def edit_description_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    description = message.text

    if len(description) > 850:
        sent_message = await message.answer(
            l10n.format_value("edit-book-error-description-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")

    response = await api.books.get_book_by_id(id_book_edited)
    book = response.result

    caption = await generate_book_caption(
        book_data=book,
        l10n=l10n,
        description=description,
    )
    caption_length = len(caption)

    if caption_length > 1024:
        sent_message = await message.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    response = await api.books.update_book(id_book_edited, description=description)
    book = response.get_model()

    await message.answer(l10n.format_value("edit-book-success"))
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, book.id_book),
    )
    await state.clear()
