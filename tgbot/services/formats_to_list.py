from typing import Dict, List, Tuple

from aiogram.types import Message
from fluent.runtime import FluentLocalization


async def formats_to_list(
    message: Message,
    l10n: FluentLocalization,
    files: List[Dict[str, str]],
) -> Tuple[List[Dict[str, str]], str]:
    """
    Adds files and their formats to the dictionary.
    :param message: Expected book file.
    :param l10n: Language set by the user.
    :param files: Files of the book.
    :return: Dictionary with files and their formats.
    """

    file = message.document.file_id
    file_format = message.document.file_name.split(".")[-1]

    if files is None:
        files = []

    if any(file["format"] == file_format for file in files):
        selected_text = "files-already-sent"
    else:
        file_dict = {"format": file_format, "file": file}
        files.append(file_dict)
        selected_text = "files-send-more"

    formats = ", ".join(f"{file['format']}" for file in files)
    text = l10n.format_value(selected_text, {"formats": formats})

    return files, text
