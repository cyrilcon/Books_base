from aiogram import types

from tgbot.services.fluent_loader import get_fluent_localization


async def set_default_commands(bot, admins: list[int]):
    """
    Set bot commands for different languages and roles (admins and normal users).
    """

    languages = ["ru", "en", "uk"]

    for language in languages:
        l10n = get_fluent_localization(language)

        # Commands for all users
        commands = [
            types.BotCommand(
                command="my_account",
                description=l10n.format_value("cmd-my-account"),
            ),
            types.BotCommand(
                command="premium", description=l10n.format_value("cmd-premium")
            ),
            types.BotCommand(
                command="search", description=l10n.format_value("cmd-search")
            ),
            types.BotCommand(
                command="booking", description=l10n.format_value("cmd-booking")
            ),
            types.BotCommand(
                command="cancel_booking",
                description=l10n.format_value("cmd-cancel-booking"),
            ),
            types.BotCommand(
                command="base_store",
                description=l10n.format_value("cmd-base-store"),
            ),
            types.BotCommand(
                command="share_base",
                description=l10n.format_value("cmd-share-base"),
            ),
            types.BotCommand(
                command="support", description=l10n.format_value("cmd-support")
            ),
            types.BotCommand(
                command="start", description=l10n.format_value("cmd-start")
            ),
            types.BotCommand(command="help", description=l10n.format_value("cmd-help")),
        ]

        # Set commands for all users
        await bot.set_my_commands(commands, language_code=language)
        if language == "ru":
            await bot.set_my_commands(commands)

        # For admins
        admin_commands = commands + [
            types.BotCommand(
                command="admin", description=l10n.format_value("cmd-admin")
            ),
        ]

        # Set commands for all admins
        for admin in admins:
            # scope = types.BotCommandScopeChatMember(chat_id=admin_id, user_id=admin_id)
            scope = types.BotCommandScopeChat(chat_id=admin)
            await bot.set_my_commands(
                admin_commands, scope=scope, language_code=language
            )
            if language == "ru":
                await bot.set_my_commands(admin_commands, scope=scope)
