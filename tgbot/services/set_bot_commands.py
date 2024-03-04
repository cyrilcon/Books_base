from aiogram import types


async def set_default_commands(bot):  # Команды из меню бота
    """
    Команды из меню бота
    :param bot: экземпляр класса Bot
    :return: команды меню бота
    """

    await bot.set_my_commands(
        [
            types.BotCommand(command="get_schedule", description="️🗓️ Отправить расписание"),
            types.BotCommand(command="set_time", description="️⏰ Выбрать время рассылки"),
            types.BotCommand(command="stop_time", description="️🚫 Остановить рассылку"),
            types.BotCommand(command="bell", description="🔔 Расписание звонков"),
            types.BotCommand(command="group", description="👥 Изменить группу для диалога"),
            types.BotCommand(command="lecturer", description="👤 Узнать полное ФИО преподавателя"),
            types.BotCommand(command="support", description="⚠️ Техподдержка"),
            types.BotCommand(command="help", description="ℹ️ Справка"),
            types.BotCommand(command="start", description="🔄 Перезапустить бота"),
        ]
    )
