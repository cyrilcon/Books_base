import pytest
from httpx import AsyncClient

from config import config
from test_users import create_user

prefix = config.api.prefix + config.api.v1.prefix + config.api.v1.orders

ORDER_DATA = {
    "id_order": 1,
    "id_user": 9223372036854775806,
    "book_title": "The Great Gatsby",
    "author_name": "F. Scott Fitzgerald",
}


@pytest.fixture
async def create_order(client: AsyncClient, create_user):
    """
    Fixture to create an order.
    """

    response = await client.post(prefix, json=ORDER_DATA)
    assert response.status_code == 201
    return response.json()


class TestOrdersSuccess:
    @pytest.mark.asyncio
    async def test_get_order_ids(self, client: AsyncClient, create_order):
        """
        Test getting the list of order IDs.
        """

        response = await client.get(prefix)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        assert create_order["id_order"] in response.json()

    @pytest.mark.asyncio
    async def test_create_order(self, client: AsyncClient, create_user):
        """
        Test creating a new order.
        """

        response = await client.post(prefix, json=ORDER_DATA)
        assert response.status_code == 201
        assert response.json()["id_order"] == ORDER_DATA["id_order"]

    @pytest.mark.asyncio
    async def test_get_orders_count(self, client: AsyncClient, create_order):
        """
        Test getting the total number of orders.
        """

        response = await client.get(f"{prefix}/count")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, int)
        assert result == 1

    @pytest.mark.asyncio
    async def test_get_order_by_position(self, client: AsyncClient, create_order):
        """
        Test getting an order by position in the database.
        """

        position = 1
        response = await client.get(f"{prefix}/position/{position}")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_order_by_id(self, client: AsyncClient, create_order):
        """
        Test getting an order by ID.
        """

        id_order = create_order["id_order"]

        response = await client.get(f"{prefix}/{id_order}")
        assert response.status_code == 200
        assert response.json()["id_order"] == id_order

    @pytest.mark.asyncio
    async def test_delete_order(self, client: AsyncClient, create_order):
        """
        Test cancelling an order by ID.
        """

        id_order = create_order["id_order"]
        response = await client.delete(f"{prefix}/{id_order}")
        assert response.status_code == 204


class TestOrdersFailure:
    @pytest.mark.asyncio
    async def test_create_order_user_not_found(self, client: AsyncClient):
        """
        Test creating an order with a non-existent user.
        """

        non_existent_id_user = 9999

        order_data = ORDER_DATA.copy()
        order_data["id_user"] = non_existent_id_user

        response = await client.post(prefix, json=order_data)
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_order_already_exists(self, client: AsyncClient, create_order):
        """
        Test creating an order with a duplicate order ID.
        """

        response = await client.post(prefix, json=ORDER_DATA)
        assert response.status_code == 409

        id_order = ORDER_DATA["id_order"]
        error_text = f"Order with ID {id_order} already exists!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_orders_count_no_orders(self, client: AsyncClient):
        """
        Test getting the total number of orders when no orders are in the database.
        """

        response = await client.get(f"{prefix}/count")
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result, int)
        assert result == 0

    @pytest.mark.asyncio
    async def test_get_order_by_position_not_found(self, client: AsyncClient):
        """
        Test getting an order by a non-existent position in the database.
        """

        non_existent_position = 9999

        response = await client.get(f"{prefix}/position/{non_existent_position}")
        assert response.status_code == 404

        error_text = (
            f"Order at position {non_existent_position} in the database not found!!"
        )
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_order_by_id_not_found(self, client: AsyncClient):
        """
        Test getting an order by a non-existent ID.
        """

        non_existent_id_order = 9999

        response = await client.get(f"{prefix}/{non_existent_id_order}")
        assert response.status_code == 404

        error_text = f"Order with ID {non_existent_id_order} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_order_not_found(self, client: AsyncClient):
        """
        Test cancelling a non-existent order.
        """

        non_existent_id_order = 9999

        response = await client.delete(f"{prefix}/{non_existent_id_order}")
        assert response.status_code == 404

        error_text = f"Order with ID {non_existent_id_order} not found!!"
        assert response.json()["detail"] == error_text
