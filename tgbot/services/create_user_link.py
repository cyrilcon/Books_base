async def create_user_link(full_name: str, username: str) -> str:
    """
    Creates a link to the user.
    :param full_name: User's full name (first name and last name).
    :param username: User's username.
    :return: User reference.
    """

    if username is not None:
        user_link = f'<a href="t.me/{username}">{full_name}</a>'
    else:
        user_link = f"<code>{full_name}</code>"

    return user_link
