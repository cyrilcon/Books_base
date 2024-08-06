import re


def is_book_article(article: str):
    """
    Checks if the string is a book article.

    An item is a string that starts with the "#" symbol
    or fully conforms to the format "#YYYY", where YYYY is four digits.

    Args:
        article (str): The string to be checked.

    Returns:
        bool: True if the string is the article of the book, otherwise False.
    """

    if article.startswith("#") or re.fullmatch(r"#\d{4}", article):
        return True
