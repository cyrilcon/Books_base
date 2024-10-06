from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class TgBot(BaseModel):
    token: str
    super_admin: int


class Redis(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: str

    def dsn(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/0"
        else:
            return f"redis://{self.host}:{self.port}/0"


class Api(BaseModel):
    url: str = "http://127.0.0.1:8000"
    prefix: str = "/api/v1"


class Chat(BaseModel):
    language_code: str

    order: str
    payment: str
    support: str


class Channel(BaseModel):
    books_base: str
    link: str
    news_en: str
    news_uk: str
    news_ru: str
    news_ro: str


class YoomoneyWallet(BaseModel):
    token: str
    number: str


class Premium(BaseModel):
    rub: int
    xtr: int


class Discount(BaseModel):
    discount_15: int
    discount_30: int
    discount_50: int
    discount_100: int


class Saturday(BaseModel):
    rub: int
    xtr: int


class Price(BaseModel):
    premium: Premium
    discount: Discount
    saturday: Saturday


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="TG_BOT__",
        extra="ignore",  # Ignore unnecessary environment variables
    )

    logging_level: str = "ERROR"
    use_redis: bool = True

    tg_bot: TgBot
    redis: Redis
    api: Api = Api()
    chat: Chat
    channel: Channel
    yoomoney_wallet: YoomoneyWallet
    price: Price


config = Config()
