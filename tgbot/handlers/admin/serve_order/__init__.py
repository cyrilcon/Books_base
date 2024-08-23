from aiogram import Router

from .serve_order_from_button import serve_from_button_router
from .serve_order_cancel import serve_order_cancel_router
from .serve_order_step_1_select_order import serve_step_1_router
from .serve_order_step_2_select_book import serve_step_2_router

serve_order_routers = Router()
serve_order_routers.include_routers(
    serve_order_cancel_router,
    serve_from_button_router,
    serve_step_1_router,
    serve_step_2_router,
)
