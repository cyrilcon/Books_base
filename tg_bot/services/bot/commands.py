from typing import List

from aiogram import Bot, types

from tg_bot.services.localization.fluent_loader import get_fluent_localization

# List of supported languages
LANGUAGES = ["ru", "en", "uk"]

# Basic commands for all users
BASE_COMMANDS = [
    "my_account",
    "my_books",
    "premium",
    "search",
    "order",
    "cancel_order",
    "base_store",
    "invite",
    "share_base",
    "news",
    "saturday",
    "support",
    "settings",
    "paysupport",
    "privacy",
    "help",
    "start",
]

# Additional command for administrators
ADMIN_COMMANDS = [
    "admin",
    "add_book",
    "edit_book",
    "delete_book",
    "send_book",
    "give_book",
    "add_blacklist",
    "remove_blacklist",
    "view_orders",
    "serve_order",
    "give_premium",
    "cancel_premium",
    "give_base",
    "take_base",
    "give_discount",
    "take_discount",
    "add_article",
    "delete_article",
    "get_profile",
    "refund",
    "add_admin",
    "remove_admin",
    "send_message",
    "get_token",
    "saturday_post",
    "broadcast",
    "test_broadcast",
    "stats",
]


def get_commands(l10n, is_admin: bool = False) -> List[types.BotCommand]:
    """
    Generate list of bot commands based on user role.

    :param l10n: Localization object for command descriptions.
    :param is_admin: Boolean flag indicating if user is an admin.
    :return: List of BotCommand objects.
    """

    commands = [
        types.BotCommand(
            command=cmd,
            description=l10n.format_value(f"command-{cmd.replace('_', '-')}"),
        )
        for cmd in BASE_COMMANDS
    ]
    if is_admin:
        admin_cmds = [
            types.BotCommand(
                command=cmd,
                description=l10n.format_value(f"command-{cmd.replace('_', '-')}"),
            )
            for cmd in ADMIN_COMMANDS
        ]
        commands.extend(admin_cmds)
    return commands


async def set_default_commands(bot: Bot, admins: List[int]):
    """
    Set bot commands for different languages and roles.

    :param bot: Bot instance to set commands for.
    :param admins: List of admin user IDs.
    """

    for language in LANGUAGES:
        l10n = get_fluent_localization(language)
        user_commands = get_commands(l10n)
        admin_commands = get_commands(l10n, is_admin=True)

        # Set commands for all users
        await bot.set_my_commands(user_commands, language_code=language)
        if language == "ru":
            await bot.set_my_commands(user_commands)

        # Set commands for admins
        for admin in admins:
            scope = types.BotCommandScopeChat(chat_id=admin)
            await bot.set_my_commands(
                admin_commands, scope=scope, language_code=language
            )
            if language == "ru":
                await bot.set_my_commands(admin_commands, scope=scope)


async def set_user_commands(bot: Bot, id_user: int, is_admin: bool = False):
    """
    Set commands for a specific user based on their admin status.

    :param bot: Bot instance to set commands for.
    :param id_user: ID of the user to set commands for.
    :param is_admin: Boolean flag indicating if user is an admin.
    """

    for language in LANGUAGES:
        l10n = get_fluent_localization(language)
        commands = get_commands(l10n, is_admin=is_admin)
        scope = types.BotCommandScopeChat(chat_id=id_user)
        await bot.set_my_commands(commands, scope=scope, language_code=language)
        if language == "ru":
            await bot.set_my_commands(commands, scope=scope)
