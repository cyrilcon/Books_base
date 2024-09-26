from typing import Dict, Any, Union

from fluent.runtime import FluentLocalization

from api.books_base_api.schemas import BookSchema
from tg_bot.services.book_formatter import BookFormatter
from tg_bot.services.fluent_loader import get_fluent_localization


async def generate_book_caption(
    book_data: Union[Dict[str, Any], BookSchema],
    l10n: FluentLocalization = get_fluent_localization("ru"),
    is_post: bool = False,
    from_user: bool = False,
    **kwargs,
):
    """
    The caption of the post for the telegram channel is formed.
    :param book_data: Dictionary with book data.
    :param l10n: Language set by the user.
    :param is_post: True - text is generated for post.
    :param from_user: True - book from user.
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
        50: {
            "message": l10n.format_value("daily-action") if is_post else "",
            "price_text": "50₽ <s>85₽</s>",
        },
        85: {
            "message": l10n.format_value("new-book-from-user") if from_user else "",
            "price_text": "85₽",
        },
    }

    intro_info = intro_config.get(price, {"message": "", "price_text": f"{price}₽"})
    intro_message = intro_info["message"] if is_post else ""
    price = intro_info["price_text"]

    authors = BookFormatter.format_authors(authors)
    formats = BookFormatter.format_file_formats(files)
    genres = BookFormatter.format_genres(genres)
    article = BookFormatter.format_article(id_book)

    caption = l10n.format_value(
        "book-caption-template",
        {
            "intro_message": intro_message,
            "title": title,
            "authors": authors,
            "description": description,
            "formats": formats,
            "price": price,
            "article": article,
            "genres": genres,
        },
    )

    return caption
