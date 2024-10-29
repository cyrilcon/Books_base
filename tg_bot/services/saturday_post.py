from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link

from config import config
from tg_bot.api_client import api
from tg_bot.keyboards.inline import deep_link_set_keyboard
from tg_bot.services import get_fluent_localization


async def saturday_post(bot: Bot):
    """
    Sends a message to the channel every Saturday with a deep link to perform certain actions.

    The function generates a deep link to execute the command and sends a photo with the given text and keyboard.

    :param bot: The instance of bot to send the message to
    """

    await api.books.update_book_price()

    l10n = get_fluent_localization("ru")
    deep_link_url = await create_start_link(bot, f"set")
    await bot.send_photo(
        chat_id=config.channel.id,
        photo=config.saturday_post,
        caption=l10n.format_value("saturday-post", {"bot_link": config.tg_bot.link}),
        reply_markup=deep_link_set_keyboard(deep_link_url=deep_link_url),
    )
