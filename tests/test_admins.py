import pytest
from httpx import AsyncClient

from config import config
from test_users import create_user

prefix = (
    config.api.prefix
    + config.api.v1.prefix
    + config.api.v1.users
    + config.api.v1.admins
)

ADMIN_DATA = {
    "id_user": 9223372036854775806,
}


@pytest.fixture
async def create_admin(client: AsyncClient, create_user):
    """
    Fixture to create an admin.
    """

    response = await client.post(prefix, json=ADMIN_DATA)
    assert response.status_code == 201
    return response.json()


class TestAdminsSuccess:
    @pytest.mark.asyncio
    async def test_get_admin_ids(self, client: AsyncClient, create_admin):
        """
        Test getting the list of admin IDs.
        """

        response = await client.get(prefix)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        assert create_admin["id_user"] in response.json()

    @pytest.mark.asyncio
    async def test_create_admin(self, client: AsyncClient, create_user):
        """
        Test adding a user to admins.
        """

        response = await client.post(prefix, json=ADMIN_DATA)
        assert response.status_code == 201
        assert response.json()["is_admin"] is True

    @pytest.mark.asyncio
    async def test_delete_admin(self, client: AsyncClient, create_admin):
        """
        Test removing a user from admins.
        """

        id_user = create_admin["id_user"]
        response = await client.delete(f"{prefix}/{id_user}")
        assert response.status_code == 204


class TestAdminsFailure:
    @pytest.mark.asyncio
    async def test_create_admin_user_not_found(self, client: AsyncClient):
        """
        Test adding a non-existent user to admins.
        """

        non_existent_id_user = 9999

        admin_data = ADMIN_DATA.copy()
        admin_data["id_user"] = non_existent_id_user

        response = await client.post(prefix, json=admin_data)
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_admin_user_is_already_admin(
        self, client: AsyncClient, create_admin
    ):
        """
        Test adding a user who is already an admin.
        """

        response = await client.post(prefix, json=ADMIN_DATA)
        assert response.status_code == 409

        id_user = ADMIN_DATA["id_user"]
        error_text = f"User with ID {id_user} is already an admin!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_admin_user_not_found(self, client: AsyncClient):
        """
        Test removing a non-existent user from admins.
        """

        non_existent_id_user = 9999

        response = await client.delete(f"{prefix}/{non_existent_id_user}")
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_delete_admin_user_not_admin(self, client: AsyncClient, create_user):
        """
        Test removing a user who is not an admin.
        """

        id_user = ADMIN_DATA["id_user"]

        response = await client.delete(f"{prefix}/{id_user}")
        assert response.status_code == 409

        error_text = f"User with ID {id_user} is not an admin!!"
        assert response.json()["detail"] == error_text
