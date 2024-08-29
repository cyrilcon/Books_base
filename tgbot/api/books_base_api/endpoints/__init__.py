__all__ = (
    "AdminsApi",
    "AuthorsApi",
    "BlacklistApi",
    "BooksApi",
    "GenresApi",
    "OrdersApi",
    "PremiumApi",
    "UsersApi",
)

from .admins import AdminsApi
from .authors import AuthorsApi
from .blacklist import BlacklistApi
from .books import BooksApi
from .genres import GenresApi
from .orders import OrdersApi
from .premium import PremiumApi
from .users import UsersApi
