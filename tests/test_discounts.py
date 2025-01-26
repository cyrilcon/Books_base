import pytest
from httpx import AsyncClient

from config import config
from test_users import create_user

prefix = (
    config.api.prefix
    + config.api.v1.prefix
    + config.api.v1.users
    + config.api.v1.discounts
)

DISCOUNT_DATA = {
    "id_user": 9223372036854775806,
    "discount_value": 30,
}


@pytest.fixture
async def create_discount(client: AsyncClient, create_user):
    """
    Fixture to giving a discount to the user.
    """

    response = await client.post(prefix, json=DISCOUNT_DATA)
    assert response.status_code == 201
    return response.json()


class TestDiscountsSuccess:
    @pytest.mark.asyncio
    async def test_create_discount(self, client: AsyncClient, create_user):
        """
        Test giving a discount to the user.
        """

        response = await client.post(prefix, json=DISCOUNT_DATA)
        assert response.status_code == 201
        assert response.json()["has_discount"] == DISCOUNT_DATA["discount_value"]

    @pytest.mark.asyncio
    async def test_delete_discount(self, client: AsyncClient, create_discount):
        """
        Test removing a discount from the user.
        """

        id_user = create_discount["id_user"]
        response = await client.delete(f"{prefix}/{id_user}")
        assert response.status_code == 204


class TestDiscountsFailure:
    @pytest.mark.asyncio
    async def test_create_discount_user_not_found(self, client: AsyncClient):
        """
        Test giving a discount to the non-existent user.
        """

        non_existent_id_user = 9999

        discount_data = DISCOUNT_DATA.copy()
        discount_data["id_user"] = non_existent_id_user

        response = await client.post(prefix, json=discount_data)
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_discount_unavailable_discount(self, client: AsyncClient):
        """
        Test giving an unavailable discount to the user.
        """

        unavailable_discount_value = 75

        discount_data = DISCOUNT_DATA.copy()
        discount_data["discount_value"] = unavailable_discount_value

        response = await client.post(prefix, json=discount_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_discount_user_already_has_discount(
        self, client: AsyncClient, create_discount
    ):
        """
        Test giving a discount to the user who already has a discount.
        """

        response = await client.post(prefix, json=DISCOUNT_DATA)
        assert response.status_code == 409

        id_user = DISCOUNT_DATA["id_user"]
        error_text = f"User with ID {id_user} already has a discount!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_discount_user_not_found(self, client: AsyncClient):
        """
        Test removing a discount from the non-existent user.
        """

        non_existent_id_user = 9999

        response = await client.delete(f"{prefix}/{non_existent_id_user}")
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_discount_user_has_no_discount(
        self, client: AsyncClient, create_user
    ):
        """
        Test removing a discount from the user who already has no discount.
        """

        id_user = DISCOUNT_DATA["id_user"]

        response = await client.delete(f"{prefix}/{id_user}")
        assert response.status_code == 409

        error_text = f"User with ID {id_user} already has no discount!!"
        assert response.json()["detail"] == error_text
