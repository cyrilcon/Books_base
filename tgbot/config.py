from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class TgBot:
    """
    Создается объект TgBot из переменных окружения.

    Атрибуты
    ----------
    :param token: Токен бота.
    :type token: Str.
    :param admins: Список админов.
    :type admins: List[int].
    :param use_redis: Использование Redis.
    :type use_redis: Bool.
    :param channel: Telegram канал.
    :type channel: Int.
    :param support_chat: Чат тех-поддержки.
    :type support_chat: Int.
    :param booking_chat: Чат с заказами.
    :type booking_chat: Int.
    """

    token: str
    admins: list[int]
    use_redis: bool
    channel: int
    support_chat: int
    booking_chat: int

    @staticmethod
    def from_env(env: Env):
        """
        Создается объект TgBot из переменных окружения.
        """

        token = env.str("BOT_TOKEN")  # Токен бота
        admins = list(map(int, env.list("ADMINS")))  # Список админов
        use_redis = env.bool("USE_REDIS")  # Использование Redis
        channel = env.int("CHANNEL")  # Telegram канал
        support_chat = env.int("SUPPORT_CHAT")  # Чат тех-поддержки
        booking_chat = env.int("BOOKING_CHAT")  # Чат с заказами
        return TgBot(
            token=token,
            admins=admins,
            use_redis=use_redis,
            channel=channel,
            support_chat=support_chat,
            booking_chat=booking_chat,
        )


@dataclass
class RedisConfig:
    """
    Класс конфигурации Redis.

    Attributes
    ----------
    redis_pass : Optional(str)
        Пароль, используемый для аутентификации в Redis.
    redis_port : Optional(int)
        Порт, на котором прослушивается сервер Redis.
    redis_host : Optional(str)
        Хост, на котором расположен сервер Redis.
    """

    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        """
        Создает и возвращает Redis DSN (имя источника данных) для данной конфигурации базы данных.
        """

        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env):
        """
        Создает объект RedisConfig из переменных окружения.
        """

        redis_pass = env.str("REDIS_PASSWORD")
        redis_port = env.int("REDIS_PORT")
        redis_host = env.str("REDIS_HOST")

        return RedisConfig(
            redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host
        )


@dataclass
class Miscellaneous:
    """
    Класс различных конфигураций.

    Этот класс содержит настройки для различных других параметров.
    Он просто служит вместилищем для параметров, которые не входят в другие категории.

    Атрибуты
    ----------
    other_params : str, optional
        Строка, используемая для хранения других различных параметров по мере необходимости (по умолчанию None).
    """

    other_params: str = None


@dataclass
class Config:
    """
    Основной класс конфигурации, объединяющий все остальные классы конфигурации.

    Этот класс содержит другие классы конфигурации, обеспечивая централизованный доступ ко всем настройкам.

    Атрибуты
    ----------
    tg_bot : TgBot
        Содержит настройки, связанные с ботом Telegram.
    Misc : Miscellaneous
        Хранит значения различных настроек.
    DB : Optional[DbConfig]
        Содержит настройки, специфичные для базы данных (по умолчанию - None).
    Redis : Optional[RedisConfig]
        Содержит настройки, специфичные для Redis (по умолчанию - None).
    """

    tg_bot: TgBot
    misc: Miscellaneous
    redis: Optional[RedisConfig] = None


def load_config(path: str = ".env") -> Config:
    """
    Эта функция принимает на вход необязательный путь к файлу и возвращает объект Config.
    :param path: Путь к env-файлу, из которого загружаются конфигурационные переменные.
    Он считывает переменные окружения из файла .env, если он указан, в противном случае - из окружения процесса.
    :return: Объект конфигурации с атрибутами, установленными в соответствии с переменными окружения.
    """

    env = Env()  # Создаётся объект Env
    env.read_env(
        path
    )  # Объект Env будет использоваться для чтения переменных окружения

    return Config(
        tg_bot=TgBot.from_env(env),
        redis=RedisConfig.from_env(env),
        misc=Miscellaneous(),
    )
