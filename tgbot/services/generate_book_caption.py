from typing import Dict, Any

from fluent.runtime import FluentLocalization

from tgbot.services import get_fluent_localization


async def generate_book_caption(
    data: Dict[str, Any],
    l10n: FluentLocalization = get_fluent_localization("ru"),
    post: bool = False,
    from_user: bool = False,
):
    """
    The caption of the post for the telegram channel is formed.
    :param data: Dictionary with book data.
    :param l10n: Language set by the user.
    :param post: True - text is generated for post.
    :param from_user: True - book from user.
    :return: Ready caption of post for telegram channel.
    """

    id_book = data.get("id_book")
    title = data.get("title")
    authors = data.get("authors")
    description = data.get("description")
    genres = data.get("genres")
    files = data.get("files")
    price = data.get("price")

    introductory_text = ""
    if price == 50:
        if post:
            introductory_text = l10n.format_value("daily-action")
        price = "50₽ <s>85₽</s>"
    elif price == 85:
        if from_user:
            introductory_text = l10n.format_value("new-book-from-user")
        price = "85₽"

    authors = ", ".join([author["author"].title() for author in authors])
    formats = ", ".join(f"{file['format']}" for file in files)
    genres = " ".join(["#" + genre["genre"] for genre in genres])
    article = "#{:04d}".format(id_book)

    caption = l10n.format_value(
        "book-caption",
        {
            "introductory_text": introductory_text,
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
