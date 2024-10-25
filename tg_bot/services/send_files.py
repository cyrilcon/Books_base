from typing import List

from aiogram import Bot
from aiogram.utils.media_group import MediaGroupBuilder

from tg_bot.api_client.schemas import FileSchema


async def send_files(bot: Bot, chat_id: int, caption: str, files: List[FileSchema]):
    """
    Divide files into groups of 10 and send them as albums.

    :param bot: Bot instance.
    :param chat_id: Telegram chat id.
    :param caption: Text to send.
    :param files: List of files to send.
    """

    # Divide files into groups of 10 and send them
    for i in range(0, len(files), 10):
        album_builder = MediaGroupBuilder()

        for index, file in enumerate(files[i : i + 10]):
            file_token = file.file_token  # Get the file token

            # If it's the last file and there is a caption, add it to the last file
            if index == len(files[i : i + 10]) - 1 and caption:
                album_builder.add_document(media=file_token, caption=caption)
            else:
                album_builder.add_document(media=file_token)

        await bot.send_media_group(chat_id=chat_id, media=album_builder.build())
