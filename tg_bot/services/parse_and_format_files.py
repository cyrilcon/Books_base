from typing import Dict, List, Tuple

from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.services.book_formatter import BookFormatter


async def parse_and_format_files(
    message: Message,
    l10n: FluentLocalization,
    files: List[Dict[str, str]],
) -> Tuple[List[Dict[str, str]], str]:
    """
    Parses a new file from the message, formats it into a structured dictionary,
    and adds it to the list of files if it's a new format.

    :param message: Message object containing the uploaded document.
    :param l10n: Language set by the user.
    :param files: List of existing formatted file dictionaries.
    :return: A tuple containing:
             - An updated list of dictionaries with file formats and IDs.
             - A localized response message indicating whether the file was added or already exists.
    """

    file_token = message.document.file_id
    file_format = message.document.file_name.split(".")[-1]

    if files is None:
        files = []

    if any(file["format"] == file_format for file in files):
        text = "add-book-error-file-already-sent"
    else:
        file_dict = {"format": file_format, "file_token": file_token}
        files.append(file_dict)
        text = "add-book-prompt-more-files"

    formats = BookFormatter.format_file_formats(files)
    text = l10n.format_value(text, {"formats": formats})

    return files, text
