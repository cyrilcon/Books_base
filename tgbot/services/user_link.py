async def create_user_link(fullname: str, username: str) -> str:
    """
    Creates a link to the user.
    :param fullname: The user's full name.
    :param username: The username of the user.
    :return: User reference.
    """

    if username is not None:
        user_link = f'<a href="t.me/{username}">{fullname}</a>'
    else:
        user_link = f"<code>{fullname}</code>"

    return user_link
