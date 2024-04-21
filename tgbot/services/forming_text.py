from aiogram.fsm.context import FSMContext


async def forming_text(
    state: FSMContext,
    price: int | str,
):
    """
    Формируется текст поста для телеграм канала.
    :param state: FSM (AddBook).
    :param price: Цена.
    :return: Готовый текст поста для телеграм канала.
    """

    data = await state.get_data()
    article = data.get("article")
    title = data.get("title")
    authors = data.get("authors")
    description = data.get("description")
    genres = data.get("genres")
    files = data.get("files")

    introductory_text = ""
    if price == "50":
        price = 50
        introductory_text = "Акция дня!!\n" "Только сегодня книга <b>50₽</b>"
    elif price == "85":
        price = 85
        introductory_text = "Добавлена новая книга по заказу пользователя!!"

    authors = ", ".join(author.title() for author in authors)
    formats = ", ".join(list(files.keys()))
    price = "50₽ <s>85₽</s>" if price == 50 else "85₽"
    genres = " ".join("#" + genre for genre in genres)

    text = (
        f"{introductory_text}\n"
        f"\n"
        f'"<code><b>{title}</b></code>"\n'
        f"<i>{authors}</i>\n"
        f"\n"
        f"{description}\n"
        f"\n"
        f"Доступные форматы: {formats}\n"
        f"\n"
        f"<b>Цена:</b> {price}\n"
        f"\n"
        f"Артикул: <code>{article}</code>\n"
        f"""{genres}"""
    )
    return text
