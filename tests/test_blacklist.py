import pytest
from httpx import AsyncClient

from config import config
from test_users import create_user

prefix = (
    config.api.prefix
    + config.api.v1.prefix
    + config.api.v1.users
    + config.api.v1.blacklist
)

BLACKLIST_DATA = {
    "id_user": 1,
}


@pytest.fixture
async def create_blacklisted_user(client: AsyncClient, create_user):
    """
    Fixture to create a blacklisted user.
    """

    response = await client.post(prefix, json=BLACKLIST_DATA)
    assert response.status_code == 201
    return response.json()


class TestBlacklistSuccess:
    @pytest.mark.asyncio
    async def test_get_blacklisted_user_ids(
        self, client: AsyncClient, create_blacklisted_user
    ):
        """
        Test getting the list of blacklisted user IDs.
        """

        response = await client.get(prefix)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        assert create_blacklisted_user["id_user"] in response.json()

    @pytest.mark.asyncio
    async def test_create_blacklist(self, client: AsyncClient, create_user):
        """
        Test adding a user to the blacklist.
        """

        response = await client.post(prefix, json=BLACKLIST_DATA)
        assert response.status_code == 201
        assert response.json()["is_blacklisted"] is True

    @pytest.mark.asyncio
    async def test_delete_blacklist(self, client: AsyncClient, create_blacklisted_user):
        """
        Test removing a user from the blacklist.
        """

        id_user = create_blacklisted_user["id_user"]
        response = await client.delete(f"{prefix}/{id_user}")
        assert response.status_code == 204


class TestBlacklistFailure:
    @pytest.mark.asyncio
    async def test_create_blacklist_user_not_found(self, client: AsyncClient):
        """
        Test adding a non-existent user to the blacklist.
        """

        non_existent_id_user = 9999

        blacklist_data = BLACKLIST_DATA.copy()
        blacklist_data["id_user"] = non_existent_id_user

        response = await client.post(prefix, json=blacklist_data)
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_blacklist_user_already_blacklisted(
        self, client: AsyncClient, create_blacklisted_user
    ):
        """
        Test adding a user who is already blacklisted.
        """

        response = await client.post(prefix, json=BLACKLIST_DATA)
        assert response.status_code == 409

        error_text = (
            f"User with ID {BLACKLIST_DATA["id_user"]} is already blacklisted!!"
        )
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_blacklist_user_not_found(self, client: AsyncClient):
        """
        Test removing a non-existent user from the blacklist.
        """

        non_existent_id_user = 9999

        response = await client.delete(f"{prefix}/{non_existent_id_user}")
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_blacklist_user_not_blacklisted(
        self, client: AsyncClient, create_user
    ):
        """
        Test removing a user who is not blacklisted.
        """

        id_user = BLACKLIST_DATA["id_user"]

        response = await client.delete(f"{prefix}/{id_user}")
        assert response.status_code == 409

        error_text = f"User with ID {id_user} is not blacklisted!!"
        assert response.json()["detail"] == error_text
