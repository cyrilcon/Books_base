from aiogram import types

from tgbot.services import get_fluent_localization


async def set_default_commands(bot, admins: list[int]):
    """
    Устанавливает команды бота для разных языков и ролей (администраторы и обычные пользователи).
    """

    languages = ["ru", "en", "uk"]

    for language in languages:
        l10n = get_fluent_localization(language)

        # Команды для всех пользователей
        commands = [
            types.BotCommand(
                command="my_account",
                description=l10n.format_value("command-my-account"),
            ),
            types.BotCommand(
                command="premium", description=l10n.format_value("command-premium")
            ),
            types.BotCommand(
                command="search", description=l10n.format_value("command-search")
            ),
            types.BotCommand(
                command="booking", description=l10n.format_value("command-booking")
            ),
            types.BotCommand(
                command="cancel_booking",
                description=l10n.format_value("command-cancel-booking"),
            ),
            types.BotCommand(
                command="base_store",
                description=l10n.format_value("command-base-store"),
            ),
            types.BotCommand(
                command="share_base",
                description=l10n.format_value("command-share-base"),
            ),
            types.BotCommand(
                command="support", description=l10n.format_value("command-support")
            ),
            types.BotCommand(
                command="start", description=l10n.format_value("command-start")
            ),
            types.BotCommand(
                command="help", description=l10n.format_value("command-help")
            ),
        ]

        # Установка команд для всех пользователей
        await bot.set_my_commands(commands, language_code=language)
        if language == "ru":
            await bot.set_my_commands(commands)

        # Команды для администраторов
        admin_commands = commands + [
            types.BotCommand(
                command="admin", description=l10n.format_value("command-admin")
            ),
        ]

        for admin in admins:
            # scope = types.BotCommandScopeChatMember(chat_id=admin_id, user_id=admin_id)
            scope = types.BotCommandScopeChat(chat_id=admin)
            await bot.set_my_commands(
                admin_commands, scope=scope, language_code=language
            )
            if language == "ru":
                await bot.set_my_commands(admin_commands, scope=scope)
