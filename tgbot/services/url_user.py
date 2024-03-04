async def get_url_user(fullname: str, username: str) -> str:
    """
    Создаётся ссылка на пользователя.
    :param fullname: Имя пользователя.
    :param username: Ник пользователя.
    :return: Ссылка на пользователя.
    """

    if username is not None:
        url_user = f"<a href=\"t.me/{username}\">{fullname}</a>"
    else:
        url_user = f"<code>{fullname}</code>"

    return url_user
