import re


def extract_username(text: str) -> str | None:
    """
    Regular expression to get user username.
    :param text: Text of the message from which wants to get username.
    :return: Correct username or None.
    """

    # pattern = r"^@([a-zA-Z](?!_)(?!.*?_{2})\w{2,30}[a-zA-Z0-9])$|^(https?:\/\/)?t\.me\/([a-zA-Z](?!_)(?!.*?_{2})\w{2,30}[a-zA-Z0-9])$|^(https?:\/\/)?([a-zA-Z](?!_)(?!.*?_{2})\w{2,30}[a-zA-Z0-9])\.t\.me\/?$"
    pattern = r"(?:@|https?://t\.me/|t\.me/)([a-zA-Z0-9_]{4,32})"
    matches = re.findall(pattern, text)

    return matches[-1] if matches else None
