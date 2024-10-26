import pytest
from httpx import AsyncClient

from config import config
from test_books import create_book_1, create_book_2
from test_premium import create_premium_user
from test_users import create_user

prefix = config.api.prefix + config.api.v1.prefix + config.api.v1.payments

PAYMENT_DATA_1 = {
    "id_payment": "463f1109-a51b-473a-9bd7-0eec7e113e7e",
    "id_user": 1,
    "price": 85,
    "currency": "RUB",
    "type": "book",
    "book_ids": [
        1,
        2,
    ],
}
PAYMENT_DATA_2 = {
    "id_payment": "585f1109-a51b-473a-9bd7-0eec7e113e7d",
    "id_user": 1,
    "price": 385,
    "currency": "XTR",
    "type": "premium",
}


@pytest.fixture
async def create_payment_1(
    client: AsyncClient, create_user, create_book_1, create_book_2
):
    """
    Fixture to create the first payment.
    """

    response = await client.post(prefix, json=PAYMENT_DATA_1)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def create_payment_2(client: AsyncClient, create_user):
    """
    Fixture to create the second payment.
    """

    response = await client.post(prefix, json=PAYMENT_DATA_2)
    assert response.status_code == 201
    return response.json()


class TestPaymentsSuccess:
    @pytest.mark.asyncio
    async def test_create_payment(
        self, client: AsyncClient, create_user, create_book_1, create_book_2
    ):
        """
        Test creating a new payment.
        """

        response = await client.post(prefix, json=PAYMENT_DATA_1)
        assert response.status_code == 201
        assert response.json()["id_payment"] == PAYMENT_DATA_1["id_payment"]
        assert isinstance(response.json()["books"], list)

        response = await client.post(prefix, json=PAYMENT_DATA_2)
        assert response.status_code == 201
        assert response.json()["id_payment"] == PAYMENT_DATA_2["id_payment"]

    @pytest.mark.asyncio
    async def test_get_payment_by_id(
        self, client: AsyncClient, create_payment_1, create_payment_2
    ):
        """
        Test getting a payment by ID.
        """

        id_payment = create_payment_1["id_payment"]

        response = await client.get(f"{prefix}/{id_payment}")
        assert response.status_code == 200
        assert response.json()["id_payment"] == id_payment
        assert isinstance(response.json()["books"], list)

        id_payment = create_payment_2["id_payment"]

        response = await client.get(f"{prefix}/{id_payment}")
        assert response.status_code == 200
        assert response.json()["id_payment"] == id_payment


class TestPaymentsFailure:
    @pytest.mark.asyncio
    async def test_create_payment_with_premium_type(self, client: AsyncClient):
        """
        Test creating a payment with type "premium" but including book_ids.
        """

        payment_data = PAYMENT_DATA_1.copy()
        payment_data["type"] = "premium"

        response = await client.post(prefix, json=payment_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_payment_with_book_type(self, client: AsyncClient):
        """
        Test creating a payment with type "book" but without book_ids.
        """

        payment_data = PAYMENT_DATA_2.copy()
        payment_data["type"] = "book"

        response = await client.post(prefix, json=payment_data)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_payment_user_not_found(self, client: AsyncClient):
        """
        Test creating a payment with non-existent user.
        """

        non_existent_id_user = 9999

        payment_data = PAYMENT_DATA_1.copy()
        payment_data["id_user"] = non_existent_id_user

        response = await client.post(prefix, json=payment_data)
        assert response.status_code == 404

        error_text = f"User with ID {non_existent_id_user} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_payment_already_exists(
        self, client: AsyncClient, create_payment_1
    ):
        """
        Test creating two payments with the same id.
        """

        payment_data = PAYMENT_DATA_2.copy()
        payment_data["id_payment"] = create_payment_1["id_payment"]

        response = await client.post(prefix, json=payment_data)
        assert response.status_code == 409

        id_payment = payment_data["id_payment"]
        error_text = f"Payment with ID {id_payment} already exists!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_payment_user_already_has_books(
        self, client: AsyncClient, create_payment_1
    ):
        """
        Test creating a payment when user already has these books.
        """

        payment_data = PAYMENT_DATA_1.copy()
        payment_data["id_payment"] = PAYMENT_DATA_2["id_payment"]

        response = await client.post(prefix, json=payment_data)
        assert response.status_code == 409

        book_ids = payment_data["book_ids"]

        error_text = f"User has already purchased books with IDs: {book_ids}!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_payment_book_not_found(
        self, client: AsyncClient, create_user
    ):
        """
        Test creating a payment with a non-existent book.
        """

        non_existent_id_book = 9999

        payment_data = PAYMENT_DATA_1.copy()
        payment_data["book_ids"] = [non_existent_id_book]

        response = await client.post(prefix, json=payment_data)
        assert response.status_code == 404

        error_text = f"Book with ID {non_existent_id_book} not found!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_create_payment_user_already_has_premium(
        self, client: AsyncClient, create_user, create_premium_user
    ):
        """
        Test creating a payment with a user who already has premium.
        """

        response = await client.post(prefix, json=PAYMENT_DATA_2)
        assert response.status_code == 409

        id_user = PAYMENT_DATA_2["id_user"]
        error_text = f"User with ID {id_user} already has premium!!"
        assert response.json()["detail"] == error_text

    @pytest.mark.asyncio
    async def test_get_payment_by_id_not_found(self, client: AsyncClient):
        """
        Test getting a payment by a non-existent ID.
        """

        non_existent_id_payment = 9999

        response = await client.get(f"{prefix}/{non_existent_id_payment}")
        assert response.status_code == 404

        error_text = f"Payment with ID {non_existent_id_payment} not found!!"
        assert response.json()["detail"] == error_text
