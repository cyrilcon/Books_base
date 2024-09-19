from datetime import datetime


def generate_id_order(id_user: int) -> int:
    """
    Generates a unique order identifier.
    :param id_user: Unique user identifier.
    :return: Unique order identifier.
    """

    timestamp = int(datetime.now().timestamp()) % 1000
    user_part = id_user % 100
    id_order = int(f"{timestamp}{user_part}")

    return id_order
