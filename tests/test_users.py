from datetime import datetime

import pytest
from httpx import AsyncClient

from config import config

prefix = config.api.prefix + config.api.v1.prefix + config.api.v1.users

USER_DATA_1 = {
    "id_user": 1,
    "full_name": "John Doe",
    "username": "john_doe",
    "language_code": "en",
}
USER_DATA_2 = {
    "id_user": 2,
    "full_name": "John Smith",
    "username": "john_smith",
    "language_code": "ru",
}


@pytest.fixture
async def create_user(client: AsyncClient):
    """
    Fixture to create a user.
    """

    response = await client.post(prefix, json=USER_DATA_1)
    assert response.status_code == 201
    return response.json()


class TestUsersSuccess:
    @pytest.mark.asyncio
    async def test_get_user_ids(self, client: AsyncClient, create_user):
        """
        Test getting the list of user IDs.
        """

        response = await client.get(prefix)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        assert create_user["id_user"] in response.json()

    @pytest.mark.asyncio
    async def test_create_user(self, client: AsyncClient):
        """
        Test creating a new user.
        """

        response = await client.post(prefix, json=USER_DATA_1)
        assert response.status_code == 201
        assert response.json()["username"] == USER_DATA_1["username"]

    @pytest.mark.asyncio
    async def test_get_user_statistics(self, client: AsyncClient, create_user):
        """
        Test getting user activity statistics
        """

        response = await client.get(f"{prefix}/stats")
        assert response.status_code == 200
        assert response.json()["total_users"] == 1

    @pytest.mark.asyncio
    async def test_get_user_by_username(self, client: AsyncClient, create_user):
        """
        Test getting a user by username.
        """

        username = create_user["username"]

        response = await client.get(f"{prefix}/username/{username}")
        assert response.status_code == 200
        assert response.json()["username"] == username

    @pytest.mark.asyncio
    async def test_get_book_ids(self, client: AsyncClient, create_user):
        """
        Test getting a list of book purchased IDs by the user.
        """

        id_user = create_user["id_user"]

        response = await client.get(f"{prefix}/{id_user}/books")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_get_order_ids_by_user(self, client: AsyncClient, create_user):
        """
        Test getting a list of order IDs by the user.
        """

        id_user = create_user["id_user"]

        response = await client.get(f"{prefix}/{id_user}/orders")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, client: AsyncClient, create_user):
        """
        Test getting a user by ID.
        """

        id_user = create_user["id_user"]

        response = await client.get(f"{prefix}/{id_user}")
        assert response.status_code == 200
        assert response.json()["id_user"] == id_user

    @pytest.mark.asyncio
    async def test_update_user(self, client: AsyncClient, create_user):
        """
        Test updating user information.
        """

        update_data = {
            "full_name": "Jane Doe",
            "last_activity_datetime": datetime.now().isoformat(),
            "referrer_id": 2,
        }

        id_user = create_user["id_user"]
        response = await client.patch(f"{prefix}/{id_user}", json=update_data)
        assert response.status_code == 200

        full_name = update_data["full_name"]
        assert response.json()["full_name"] == full_name


class TestUsersFailure:
    @pytest.mark.asyncio
    async def test_create_user_already_exists(self, client: AsyncClient, create_user):
        """
        Test creating two users with the same id.
        """

        id_user = create_user["id_user"]

        user_data_2 = USER_DATA_2.copy()
        user_data_2["id_user"] = id_user

        response = await client.post(prefix, json=user_data_2)
        assert response.status_code == 409

        error_text = f"User with ID {id_user} already exists!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_user_username_already_exists(
        self, client: AsyncClient, create_user
    ):
        """
        Test creating two users with the same username.
        """

        username = create_user["username"]

        user_data_2 = USER_DATA_2.copy()
        user_data_2["username"] = username

        response = await client.post(prefix, json=user_data_2)
        assert response.status_code == 409

        error_text = f"User with username '@{username}' already exists!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_user_username_too_short(self, client: AsyncClient):
        """
        Test creating a user with too short username.
        """

        user_with_too_long_username_data = USER_DATA_2.copy()
        user_with_too_long_username_data["username"] = "non"

        response = await client.post(prefix, json=user_with_too_long_username_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_user_username_too_long(self, client: AsyncClient):
        """
        Test creating a user with too long username.
        """

        user_with_too_long_username_data = USER_DATA_2.copy()
        user_with_too_long_username_data["username"] = "too_long_username" * 3

        response = await client.post(prefix, json=user_with_too_long_username_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_user_full_name_too_long(self, client: AsyncClient):
        """
        Test creating a user with too long full_name.
        """

        user_with_too_long_full_name_data = USER_DATA_2.copy()
        user_with_too_long_full_name_data["full_name"] = "too_long_full_name" * 20

        response = await client.post(prefix, json=user_with_too_long_full_name_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_user_language_code_too_long(self, client: AsyncClient):
        """
        Test creating a user with too long language_code.
        """

        user_with_too_long_language_code_data = USER_DATA_2.copy()
        user_with_too_long_language_code_data["language_code"] = "english_english"

        response = await client.post(prefix, json=user_with_too_long_language_code_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_user_by_username_not_found(self, client: AsyncClient):
        """
        Test getting a user by a non-existent username.
        """

        non_existent_username = "non_existent_user"

        response = await client.get(f"{prefix}/username/{non_existent_username}")
        assert response.status_code == 404

        error_text = f"User with username '@{non_existent_username}' not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_book_ids_not_fount(self, client: AsyncClient):
        """
        Test getting a list of book purchased IDs by a non-existent user.
        """

        non_existent_id_user = 9999

        response = await client.get(f"{prefix}/{non_existent_id_user}/books")
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_order_ids_by_user_not_fount(self, client: AsyncClient):
        """
        Test getting a list of order IDs by a non-existent user.
        """

        non_existent_id_user = 9999

        response = await client.get(f"{prefix}/{non_existent_id_user}/orders")
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, client: AsyncClient):
        """
        Test getting a user by a non-existent ID.
        """

        non_existent_id_user = 9999

        response = await client.get(f"{prefix}/{non_existent_id_user}")
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, client: AsyncClient):
        """
        Test updating a user by a non-existent ID.
        """

        non_existent_id_user = 9999
        update_data = {
            "username": "john_doe_cool",
            "last_activity_datetime": datetime.now().isoformat(),
        }

        response = await client.patch(
            f"{prefix}/{non_existent_id_user}", json=update_data
        )
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_update_user_incomplete_data(self, client: AsyncClient, create_user):
        """
        Test updating a user with incomplete data.
        """

        incomplete_update_data = {
            "username": "john_doe_cool",
        }

        id_user = create_user["id_user"]
        response = await client.patch(
            f"{prefix}/{id_user}", json=incomplete_update_data
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_user_invalid_referrer_id(
        self, client: AsyncClient, create_user
    ):
        """
        Test updating a user with referrer_id equal to id_user.
        """

        id_user = create_user["id_user"]
        update_data = {
            "last_activity_datetime": datetime.now().isoformat(),
            "referrer_id": id_user,
        }

        response = await client.patch(f"{prefix}/{id_user}", json=update_data)
        assert response.status_code == 400

        error_text = (
            "A user cannot refer themselves: 'referrer_id' must not equal 'id_user'!!"
        )
        assert response.json()["detail"] == error_text
