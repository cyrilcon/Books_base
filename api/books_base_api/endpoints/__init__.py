__all__ = (
    "AdminsApi",
    "ArticlesApi",
    "AuthorsApi",
    "BlacklistApi",
    "BooksApi",
    "DiscountsApi",
    "GenresApi",
    "OrdersApi",
    "PaymentsApi",
    "PremiumApi",
    "UsersApi",
)

from .admins import AdminsApi
from .articles import ArticlesApi
from .authors import AuthorsApi
from .blacklist import BlacklistApi
from .books import BooksApi
from .discounts import DiscountsApi
from .genres import GenresApi
from .orders import OrdersApi
from .payments import PaymentsApi
from .premium import PremiumApi
from .users import UsersApi
