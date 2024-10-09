from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

search_pagination_info_router = Router()


# TODO: НЕ УДАЛЯТЬ И  НЕ СОХРАНЯТЬ СООБЩЕНИЕ С КЛАВИАТУРОЙ
@search_pagination_info_router.callback_query(F.data.startswith("pagination_info"))
async def search_pagination_info(call: CallbackQuery, l10n: FluentLocalization):
    page = call.data.split(":")[-2]
    all_pages = call.data.split(":")[-1]

    text = l10n.format_value(
        "search-pagination-info",
        {
            "page": page,
            "all_pages": all_pages,
        },
    )
    await call.answer(text, show_alert=True)
