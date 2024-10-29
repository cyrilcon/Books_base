from datetime import timedelta, timezone

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    admins: str = "/admins"
    articles: str = "/articles"
    authors: str = "/authors"
    blacklist: str = "/blacklist"
    books: str = "/books"
    discounts: str = "/discounts"
    genres: str = "/genres"
    orders: str = "/orders"
    payments: str = "/payments"
    premium: str = "/premium"
    users: str = "/users"


class ApiTags(BaseModel):
    admins: str = "Admins"
    articles: str = "Articles"
    authors: str = "Authors"
    blacklist: str = "Blacklist"
    books: str = "Books"
    discounts: str = "Discounts"
    genres: str = "Genres"
    orders: str = "Orders"
    payments: str = "Payments"
    premium: str = "Premium"
    users: str = "Users"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    tags: ApiTags = ApiTags()
    v1: ApiV1Prefix = ApiV1Prefix()
    run: RunConfig = RunConfig()


class TgBotConfig(BaseModel):
    token: str
    super_admin: int
    link: str


class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str
    database: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    def construct_url(self, driver="asyncpg", host=None, port=5432) -> str:
        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Redis(BaseModel):
    host: str = "localhost"
    port: int = 6379
    password: str

    def dsn(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/0"
        else:
            return f"redis://{self.host}:{self.port}/0"


class Chat(BaseModel):
    language_code: str
    order: int
    payment: int
    support: int


class Channel(BaseModel):
    id: int
    link: str


class YoomoneyWallet(BaseModel):
    token: str
    number: str


class Main(BaseModel):
    rub: int
    xtr: int


class Daily(BaseModel):
    rub: int
    xtr: int


class Book(BaseModel):
    main: Main
    daily: Daily


class Premium(BaseModel):
    rub: int
    xtr: int


class Discount(BaseModel):
    discount_15: int
    discount_30: int
    discount_50: int
    discount_100: int


class Set(BaseModel):
    rub: int
    xtr: int


class Price(BaseModel):
    book: Book
    premium: Premium
    discount: Discount
    set: Set


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )

    api: ApiConfig
    tg_bot: TgBotConfig

    db: DatabaseConfig
    redis: Redis
    chat: Chat
    channel: Channel
    yoomoney_wallet: YoomoneyWallet
    price: Price

    saturday_post: str
    logging_level: str = "ERROR"
    timezone_offset: int = Field(description="Time zone offset relative to UTC")

    @property
    def timezone(self):
        return timezone(timedelta(hours=self.timezone_offset))


config = Config()
