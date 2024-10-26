from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.api_v1 import crud
from api.api_v1.schemas import (
    PaymentCurrencyEnum,
    PaymentTypeEnum,
    PaymentCreate,
    PaymentSchema,
)
from database.models import User, Payment, BookPayment, Premium


async def _get_payment_by_id(session: AsyncSession, id_payment: str) -> Payment | None:
    """
    Helper function to get a payment by ID.
    """

    stmt = (
        select(Payment)
        .where(Payment.id_payment == id_payment)
        .options(selectinload(Payment.books))
    )
    result: Result = await session.execute(stmt)
    payment = result.scalar_one_or_none()
    return payment


async def _get_books_by_payment(
    session: AsyncSession, id_payment: str
) -> List[BookPayment]:
    """
    Helper function to get the list of books by payment ID.
    """

    stmt = (
        select(BookPayment)
        .where(BookPayment.id_payment == id_payment)
        .options(selectinload(BookPayment.book))
    )
    result: Result = await session.execute(stmt)
    books = result.scalars().all()
    return list(books)


async def create_payment(
    session: AsyncSession, payment_data: PaymentCreate
) -> PaymentSchema:
    """
    Create a new payment.
    """

    # Check if the user exists
    user = await session.get(User, payment_data.id_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {payment_data.id_user} not found!!",
        )

    # Create a payment record that matches the database structure
    payment = Payment(
        id_payment=payment_data.id_payment,
        id_user=payment_data.id_user,
        price=payment_data.price,
        currency=payment_data.currency.value,  # Convert the string to Enum
    )

    try:
        session.add(payment)

        # Logic for payment type “book”
        books = []
        if payment_data.type == PaymentTypeEnum.BOOK:
            # Get a list of books already bought by the user
            purchased_book_ids = await crud.users.get_book_ids(
                session=session,
                id_user=payment_data.id_user,
            )

            # Check if the books in payment_data.book_ids have already been bought
            already_purchased_books = [
                book_id
                for book_id in payment_data.book_ids
                if book_id in purchased_book_ids
            ]

            if already_purchased_books:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User has already purchased books with IDs: {already_purchased_books}!!",
                )

            # Handling books that haven't been bought yet
            for id_book in payment_data.book_ids:
                # Add records to the BookPayment table
                book_payment = BookPayment(
                    id_payment=payment.id_payment,
                    id_book=id_book,
                )
                session.add(book_payment)

                # Get the book information to return in the reply
                book = await crud.books.get_book_details(
                    session=session,
                    id_book=id_book,
                )
                if not book:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with ID {id_book} not found!!",
                    )
                books.append(book)

        # Logic for payment type “premium”
        elif payment_data.type == PaymentTypeEnum.PREMIUM:
            # Check if there is already a user record in Premium
            existing_premium_user = await session.get(Premium, payment_data.id_user)
            if existing_premium_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User with ID {payment_data.id_user} already has premium!!",
                )

            # If the user does not have a premium yet, create a record in the Premium table
            premium_entry = Premium(
                id_user=payment_data.id_user,
                id_payment=payment.id_payment,
            )
            session.add(premium_entry)

        await session.commit()
        await session.refresh(payment)

        # Prepare and return the PaymentSchema object
        payment_schema = PaymentSchema(
            id_payment=payment.id_payment,
            id_user=payment.id_user,
            price=payment.price,
            currency=PaymentCurrencyEnum(
                payment.currency
            ),  # Convert the string to Enum
            type=payment_data.type,  # Transmit the type based on the transmitted data
            books=books if payment_data.type == PaymentTypeEnum.BOOK else None,
            payment_datetime=payment.payment_datetime,
        )
        return payment_schema

    except IntegrityError:
        # Rollback the transaction in case of an error
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Payment with ID {payment.id_payment} already exists!!",
        )


async def get_payment_by_id(
    session: AsyncSession, id_payment: str
) -> PaymentSchema | None:
    """
    Get a payment by ID.
    """

    payment = await _get_payment_by_id(session, id_payment)

    if payment is None:
        return None

    books = []
    if payment.books:
        book_payments = await _get_books_by_payment(session, id_payment)

        for book_payment in book_payments:
            book_details = await crud.books.get_book_details(
                session=session, id_book=book_payment.id_book
            )
            if book_details:
                books.append(book_details)

    payment_schema = PaymentSchema(
        id_payment=payment.id_payment,
        id_user=payment.id_user,
        price=payment.price,
        currency=PaymentCurrencyEnum(payment.currency),
        type=PaymentTypeEnum.BOOK if books else PaymentTypeEnum.PREMIUM,
        books=books if books else None,
        payment_datetime=payment.payment_datetime,
    )
    return payment_schema
