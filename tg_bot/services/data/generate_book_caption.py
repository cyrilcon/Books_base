from typing import Dict, Any, Union

from fluent.runtime import FluentLocalization

from config import config
from tg_bot.api_client import api
from api.api_v1.schemas import BookSchema, UserSchema
from tg_bot.services.data.book_formatter import BookFormatter
from tg_bot.services.localization.fluent_loader import get_fluent_localization


async def generate_book_caption(
    book_data: Union[Dict[str, Any], BookSchema],
    l10n: FluentLocalization = get_fluent_localization("ru"),
    is_post: bool = False,
    from_user: bool = False,
    user: UserSchema = None,
    **kwargs,
):
    """
    The caption of the post for the telegram channel is formed.
    :param book_data: Dictionary with book data.
    :param l10n: Language set by the user.
    :param is_post: True - text is generated for post.
    :param from_user: True - book from user.
    :param user: User instance.
    :param kwargs: Additional parameters that may override book_data.
    :return: Ready caption of post for telegram channel.
    """

    if isinstance(book_data, BookSchema):
        book_data = book_data.model_dump()

    id_book = kwargs.get("id_book", book_data.get("id_book"))
    title = kwargs.get("title", book_data.get("title"))
    authors = kwargs.get("authors", book_data.get("authors"))
    description = kwargs.get("description", book_data.get("description"))
    genres = kwargs.get("genres", book_data.get("genres"))
    files = kwargs.get("files", book_data.get("files"))
    price = kwargs.get("price", book_data.get("price"))

    intro_config = {
        0: {
            "message": "",
            "price_text": "",
        },
        config.price.book.daily.rub: {
            "message": l10n.format_value("daily-action") if is_post else "",
            "price_text": f"\n{l10n.format_value("price", {"price": price})}\n",
        },
        config.price.book.main.rub: {
            "message": l10n.format_value("new-book-from-user") if from_user else "",
            "price_text": f"\n{l10n.format_value("price", {"price": price})}\n",
        },
    }

    intro_info = intro_config.get(price, {"message": "", "price_text": f"{price}₽"})
    intro_message = intro_info["message"] if is_post else ""
    price_text = intro_info["price_text"]

    if user:
        response = await api.users.get_book_ids(id_user=user.id_user)
        book_ids = response.result

        if user.is_premium:
            price_text = f"\n{l10n.format_value("free-with-premium")}\n"
        elif id_book in book_ids:
            price_text = ""
        elif user.has_discount and price != config.price.book.daily.rub:
            prices = {
                15: round(0.85 * config.price.book.main.rub),
                30: round(0.70 * config.price.book.main.rub),
                50: round(0.50 * config.price.book.main.rub),
                100: 0,
            }
            price = prices.get(user.has_discount)
            price_text = f"\n{l10n.format_value("price", {"price": price})}\n"

    authors = BookFormatter.format_authors(authors)
    formats = BookFormatter.format_file_formats(files)
    genres = BookFormatter.format_genres(genres)
    article = BookFormatter.format_article(id_book)

    book_caption = l10n.format_value(
        "book-caption-template",
        {
            "intro_message": intro_message,
            "title": title,
            "authors": authors,
            "description": description,
            "formats": formats,
            "price": price_text,
            "article": article,
            "genres": genres,
        },
    )

    return book_caption
