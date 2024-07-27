from aiogram import Bot
from aiogram.types import InputMediaDocument


async def send_files_in_groups(bot: Bot, chat_id: int, files: list, text: str = None):
    """
    Divide files into groups of 10 and send them as albums.

    :param bot: Bot instance.
    :param chat_id: Recipient user id.
    :param files: List of files to send.
    :param text: Text to send.
    """

    # Divide files into groups of 10
    for i in range(0, len(files), 10):
        media_group = create_media_group(files[i : i + 10])

        # If it's the last group and there is text, add it to the last file
        if i + 10 >= len(files) and text:
            media_group[-1].caption = text

        await bot.send_media_group(chat_id=chat_id, media=media_group)


def create_media_group(files: list) -> list:
    """
    Create a media group for sending.

    :param files: List of files to send.
    :return: List of InputMediaDocument objects.
    """

    media_group = []
    for file_id in files:
        media_group.append(InputMediaDocument(media=file_id))
    return media_group
