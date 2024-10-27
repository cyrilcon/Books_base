import pytest
from httpx import AsyncClient

from config import config
from test_users import create_user

prefix = (
    config.api.prefix
    + config.api.v1.prefix
    + config.api.v1.users
    + config.api.v1.premium
)

PREMIUM_DATA = {
    "id_user": 1,
}


@pytest.fixture
async def create_premium_user(client: AsyncClient, create_user):
    """
    Fixture to create a premium user.
    """

    response = await client.post(prefix, json=PREMIUM_DATA)
    assert response.status_code == 201
    return response.json()


class TestPremiumSuccess:
    @pytest.mark.asyncio
    async def test_create_premium(self, client: AsyncClient, create_user):
        """
        Test assigning a user to premium.
        """

        response = await client.post(prefix, json=PREMIUM_DATA)
        assert response.status_code == 201
        assert response.json()["is_premium"] is True

    @pytest.mark.asyncio
    async def test_delete_premium(self, client: AsyncClient, create_premium_user):
        """
        Test removing a user from the list of premium users.
        """

        id_user = create_premium_user["id_user"]
        response = await client.delete(f"{prefix}/{id_user}")
        assert response.status_code == 204


class TestPremiumFailure:
    @pytest.mark.asyncio
    async def test_create_premium_user_not_found(self, client: AsyncClient):
        """
        Test assigning a non-existent user to premium.
        """

        non_existent_id_user = 9999

        premium_data = PREMIUM_DATA.copy()
        premium_data["id_user"] = non_existent_id_user

        response = await client.post(prefix, json=premium_data)
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_premium_user_already_has_premium(
        self, client: AsyncClient, create_premium_user
    ):
        """
        Test assigning a user who already has premium.
        """

        response = await client.post(prefix, json=PREMIUM_DATA)
        assert response.status_code == 409

        id_user = PREMIUM_DATA["id_user"]
        error_text = f"User with ID {id_user} already has premium!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_premium_user_not_found(self, client: AsyncClient):
        """
        Test removing a non-existent user from the premium list.
        """

        non_existent_id_user = 9999

        response = await client.delete(f"{prefix}/{non_existent_id_user}")
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_premium_user_not_premium(
        self, client: AsyncClient, create_user
    ):
        """
        Test removing a user who is not in the premium list.
        """

        id_user = PREMIUM_DATA["id_user"]

        response = await client.delete(f"{prefix}/{id_user}")
        assert response.status_code == 409

        error_text = f"User with ID {id_user} is not assigned to premium!!"
        assert response.json()["detail"] == error_text
