from typing import Tuple, Optional

from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.services import create_user_link


async def get_order_info(
    l10n: FluentLocalization,
    position: int = 1,
) -> Tuple[int, Optional[int], Optional[str]]:
    """
    Receive order information and total number of orders.

    :param l10n: Language set by the user.
    :param position: Order position in the database.
    :return: A tuple containing the number of orders, unique order identifier and text with order information.
    """

    response = await api.orders.get_orders_count()
    orders_count = response.result

    if orders_count == 0:
        return orders_count, None, None

    response = await api.orders.get_order_by_position(position=position)
    order = response.get_model()
    id_order = order.id_order

    response = await api.users.get_user_by_id(id_user=order.id_user)
    user = response.get_model()

    user_link = create_user_link(user.full_name, user.username)

    text = l10n.format_value(
        "order-information-template",
        {
            "user_link": user_link,
            "id_user": str(order.id_user),
            "book_title": order.book_title,
            "author_name": order.author_name,
            "id_order": str(id_order),
        },
    )
    return orders_count, id_order, text
