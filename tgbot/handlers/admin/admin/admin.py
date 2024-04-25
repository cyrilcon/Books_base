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
        # "💶 Изменить цену — /change_price\n"
        # "\n"
        # "🗒️ Обслужить заказ — /serve\n"
        # "\n"
        # "🕵🏻 Посмотреть заказы — /check_booking\n"
        # "\n"
        "📕 Удалить книгу — /delete_book\n"
        # "\n"
        # "📙 Отправить книгу — /send_book\n"
        # "\n"
        # "📗 Подарить книгу — /give_book\n"
        # "\n"
        # "📂 Отправить файлы — /send_files\n"
        # "\n"
        # "⚜️ Подарить PREMIUM — /give_premium\n"
        # "\n"
        # "♦️ Отменить PREMIUM — \n"
        # "/cancel_premium\n"
        # "\n"
        # "📚 Субботний пост — /action\n"
        # "\n"
        # "👨🏾‍💻 Сообщение от админа — \n"
        # "/message_from_admin"
    )
