from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.filters import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("admin"))
async def admin(message: Message):
    """
    Обработка команды /admin.
    :param message: Команда /admin.
    :return: Сообщение для админа.
    """

    await message.answer(
        "📖 Добавить книгу — /add_book\n"
        "\n"
        "♻️ Изменить данные о книге — /edit_book\n"
        "\n"
        "📕 Удалить книгу — /delete_book\n"
        # "\n"
        # "📙 Отправить книгу — /send_book\n"
        # "\n"
        # "📗 Подарить книгу — /give_book\n"
        "\n"
        "\n"
        "❌ Добавить в чёрный список – /add_blacklist\n"
        "\n"
        "❎ Удалить из чёрного списка – /remove_blacklist\n"
        "\n"
        "\n"
        "📬 Посмотреть заказы — /check_booking\n"
        "\n"
        "\n"
        "📂 Отправить файлы — /send_files\n"
        "\n"
        # "⚜️ Подарить PREMIUM — /give_premium\n"
        # "\n"
        # "♦️ Отменить PREMIUM — /cancel_premium\n"
        # "\n"
        # "📚 Субботний пост — /action\n"
        # "\n"
        "\n"
        "💎 Выдать base — /give_base\n"
        "\n"
        "\n"
        "🪪 Получить информацию о пользователе — /get_profile\n"
        "\n"
        "\n"
        "🙋🏼 Назначить администратора — /add_admin\n"
        "\n"
        "🙅🏼 Удалить администратора — /remove_admin\n"
        "\n"
        "\n"
        "🧑🏼‍💻 Сообщение от админа — /send_message"
    )
