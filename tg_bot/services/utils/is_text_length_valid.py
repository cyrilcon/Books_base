import re


def is_text_length_valid(html_text: str) -> bool:
    """
    Checks if the length of the text without HTML tags does not exceed 1024 characters.

    :param html_text: String containing HTML tags.
    :return: True if the text length without HTML tags is less than or equal to 1024, otherwise False.
    """

    clean_text = re.sub(r"<[^>]+>", "", html_text)  # Remove HTML tags
    return len(clean_text) <= 1024
