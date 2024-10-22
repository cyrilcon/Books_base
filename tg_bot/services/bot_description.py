from aiogram import Bot

from tg_bot.services.fluent_loader import get_fluent_localization

# List of supported languages
LANGUAGES = ["ru", "en", "uk"]


async def set_bot_description(bot: Bot):
    """
    Set bot description.

    :param bot: Bot instance to set description.
    """

    await set_short_description(bot)

    for language in LANGUAGES:
        l10n = get_fluent_localization(language)
        await bot.set_my_description(
            l10n.format_value("bot-description"),
            language_code=language,
        )
        if language == "ru":
            await bot.set_my_description(l10n.format_value("bot-description"))


async def set_short_description(bot: Bot):
    """
    Set bot short description.

    :param bot: Bot instance to set description.
    """

    for language in LANGUAGES:
        l10n = get_fluent_localization(language)
        await bot.set_my_short_description(
            l10n.format_value("bot-short-description"),
            language_code=language,
        )
        if language == "ru":
            await bot.set_my_short_description(
                l10n.format_value("bot-short-description")
            )
