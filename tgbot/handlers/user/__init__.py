from aiogram import Router

from .start import start_router

user_routers = Router()
user_routers.include_routers(
    start_router,  # Must be the first
    # search_routers,  # Must be the latest
)
