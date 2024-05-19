from fluent.runtime import FluentLocalization

from tgbot.services import get_fluent_localization


async def forming_text(
    data: dict,
    l10n: FluentLocalization = get_fluent_localization("ru"),
    post: bool = True,  # TODO: поменять на False
    from_user: bool = False,
):
    """
    Формируется текст поста для телеграм канала.
    :param data: Словарь с данными о книге.
    :param l10n: Язык установленный у пользователя.
    :param post: True – текст формируется для поста.
    :param from_user: True – книга от пользователя.
    :return: Готовый текст поста для телеграм канала.
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
    id_book = "#{:04d}".format(id_book)

    text = l10n.format_value(
        "full-book-description",
        {
            "introductory_text": introductory_text,
            "title": title,
            "authors": authors,
            "description": description,
            "formats": formats,
            "price": price,
            "id_book": id_book,
            "genres": genres,
        },
    )

    return text
