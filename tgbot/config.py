from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    use_redis: bool
    logging_level: str
    tg_channel: int
    support_chat: int
    booking_chat: int
    super_admin: int

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """

        token = env.str("BOT_TOKEN")
        use_redis = env.bool("USE_REDIS")
        logging_level = env.str("LOGGING_LEVEL")
        tg_channel = env.int("TG_CHANNEL")
        support_chat = env.int("SUPPORT_CHAT")
        booking_chat = env.int("BOOKING_CHAT")
        super_admin = env.int("SUPER_ADMIN")
        return TgBot(
            token=token,
            use_redis=use_redis,
            logging_level=logging_level,
            tg_channel=tg_channel,
            support_chat=support_chat,
            booking_chat=booking_chat,
            super_admin=super_admin,
        )


@dataclass
class RedisConfig:
    """
    Redis configuration class.

    Attributes
    ----------
    redis_pass : Optional(str)
        The password used to authenticate with Redis.
    redis_port : Optional(int)
        The port where Redis server is listening.
    redis_host : Optional(str)
        The host where Redis server is located.
    """

    redis_pass: Optional[str]
    redis_port: Optional[int]
    redis_host: Optional[str]

    def dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """

        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        else:
            return f"redis://{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env):
        """
        Creates the RedisConfig object from environment variables.
        """

        redis_pass = env.str("REDIS_PASSWORD")
        redis_port = env.int("REDIS_PORT")
        redis_host = env.str("REDIS_HOST")

        return RedisConfig(
            redis_pass=redis_pass, redis_port=redis_port, redis_host=redis_host
        )


@dataclass
class Api:
    """
    API configuration class.

    This class holds the configuration for the external API used by the application.

    Attributes
    ----------
    url : str
        The base URL of the external API.
    prefix : str
        ...
    """

    url: str
    prefix: str = "/api/v1"

    @staticmethod
    def from_env(env: Env):
        """
        Creates the Api object from environment variables.
        """

        url = env.str("API_URL")
        prefix = env.str("API_PREFIX")

        return Api(
            url=url,
            prefix=prefix,
        )


@dataclass
class Miscellaneous:
    """
    Miscellaneous configuration class.

    This class holds settings for various other parameters.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes
    ----------
    other_params : str, optional
        A string used to hold other various parameters as required (default is None).
    """

    other_params: str = None


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    api : Api
        Holds the settings specific to the external API.
    misc : Miscellaneous
        Holds the values for miscellaneous settings.
    redis : Optional[RedisConfig]
        Holds the settings specific to Redis (default is None).
    """

    tg_bot: TgBot
    api: Api
    misc: Miscellaneous
    redis: Optional[RedisConfig] = None


def load_config(path: str = ".env") -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot.from_env(env),
        redis=RedisConfig.from_env(env),
        api=Api.from_env(env),
        misc=Miscellaneous(),
    )


config = load_config(".env")
