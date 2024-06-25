import re


def check_username(text: str) -> str | None:
    """
    Регулярное выражение для получения username пользователя

    :param text: Текст сообщения из которого нужно получить username
    :return: Correct username or None
    """

    pattern = r"^@([a-zA-Z](?!_)(?!.*?_{2})\w{2,30}[a-zA-Z0-9])$|^(https?:\/\/)?t\.me\/([a-zA-Z](?!_)(?!.*?_{2})\w{2,30}[a-zA-Z0-9])$|^(https?:\/\/)?([a-zA-Z](?!_)(?!.*?_{2})\w{2,30}[a-zA-Z0-9])\.t\.me\/?$"
    match = re.search(pattern, text)

    if match:
        return next((group for group in match.groups() if group), None)
    return None
