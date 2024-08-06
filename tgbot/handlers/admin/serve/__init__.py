from aiogram import Router

from .serve_1_select_booking import serve_router_1
from .serve_2_send_book import serve_router_2
from .serve_cancel import serve_cancel_router

serve_routers = Router()
serve_routers.include_routers(
    serve_cancel_router,
    serve_router_1,
    serve_router_2,
)
