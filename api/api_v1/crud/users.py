from datetime import datetime, timezone, timedelta
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.api_v1.schemas import UserCreate, UserUpdate, UserSchema, UserStats
from database.models import User, BookPayment, Payment, Order


async def _get_user_by_id_or_username(
    session: AsyncSession, id_user: int = None, username: str = None
) -> User | None:
    """
    Helper function to get a user by ID or username.
    """

    stmt = select(User).options(
        selectinload(User.discount),
        selectinload(User.admin),
        selectinload(User.premium),
        selectinload(User.blacklist),
    )

    if id_user:
        stmt = stmt.where(User.id_user == id_user)
    elif username:
        stmt = stmt.where(User.username == username)

    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def get_user_ids(session: AsyncSession) -> List[int]:
    """
    Get a list of user IDs.
    """

    stmt = select(User.id_user)
    result: Result = await session.execute(stmt)
    user_ids = result.scalars().all()
    return list(user_ids)


async def create_user(session: AsyncSession, user_data: UserCreate) -> UserSchema:
    """
    Create a new user.
    """

    user = User(**user_data.model_dump())

    try:
        session.add(user)
        await session.commit()
        user_details = await get_user_details(session, id_user=user.id_user)
        return user_details
    except IntegrityError as e:
        await session.rollback()
        if "username" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with username '@{user.username}' already exists!!",
            )
        elif "id_user" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with ID {user.id_user} already exists!!",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conflict in user data!!",
            )


async def get_user_statistics(session: AsyncSession) -> UserStats:
    """
    Get user activity statistics.
    """

    # Current time
    now = datetime.now(timezone.utc)

    # Time periods
    one_hour_ago = now - timedelta(hours=1)
    one_day_ago = now - timedelta(days=1)
    one_week_ago = now - timedelta(weeks=1)
    one_month_ago = now - timedelta(days=30)

    # Get the number of users active in the last hour
    stmt_last_hour = select(func.count(User.id_user)).where(
        User.last_activity_datetime >= one_hour_ago
    )
    result_last_hour = await session.execute(stmt_last_hour)
    active_last_hour = result_last_hour.scalar()

    # Get the number of users active in the last 24 hours
    stmt_last_24_hours = select(func.count(User.id_user)).where(
        User.last_activity_datetime >= one_day_ago
    )
    result_last_24_hours = await session.execute(stmt_last_24_hours)
    active_last_24_hours = result_last_24_hours.scalar()

    # Get the number of users active in the last week
    stmt_last_week = select(func.count(User.id_user)).where(
        User.last_activity_datetime >= one_week_ago
    )
    result_last_week = await session.execute(stmt_last_week)
    active_last_week = result_last_week.scalar()

    # Get the number of users active in the last month
    stmt_last_month = select(func.count(User.id_user)).where(
        User.last_activity_datetime >= one_month_ago
    )
    result_last_month = await session.execute(stmt_last_month)
    active_last_month = result_last_month.scalar()

    # Get the total number of users in the database
    stmt_total_users = select(func.count(User.id_user))
    result_total_users = await session.execute(stmt_total_users)
    total_users = result_total_users.scalar()

    # Return the statistics as a UserStatistics object
    return UserStats(
        active_last_hour=active_last_hour,
        active_last_24_hours=active_last_24_hours,
        active_last_week=active_last_week,
        active_last_month=active_last_month,
        total_users=total_users,
    )


async def get_user_details(
    session: AsyncSession, id_user: int = None, username: str = None
) -> UserSchema | None:
    """
    Get user details by ID or username.
    """

    user = await _get_user_by_id_or_username(
        session, id_user=id_user, username=username
    )

    if not user:
        return None
    if user.discount:
        has_discount = user.discount.discount_value
    else:
        has_discount = False

    return UserSchema(
        id_user=user.id_user,
        full_name=user.full_name,
        username=user.username,
        language_code=user.language_code,
        registration_datetime=user.registration_datetime,
        last_activity_datetime=user.last_activity_datetime,
        base_balance=user.base_balance,
        referrer_id=user.referrer_id,
        is_admin=bool(user.admin),
        is_blacklisted=bool(user.blacklist),
        is_premium=bool(user.premium),
        has_discount=has_discount,
    )


async def get_user_by_id(session: AsyncSession, id_user: int) -> User | None:
    """
    Get a user by ID.
    """

    return await _get_user_by_id_or_username(session, id_user=id_user)


async def get_book_ids(session: AsyncSession, id_user: int) -> List[int]:
    """
    Get a list of book purchased IDs by the user.
    """

    stmt = (
        select(BookPayment.id_book)
        .join(Payment, Payment.id_payment == BookPayment.id_payment)
        .where(Payment.id_user == id_user)
        .order_by(Payment.payment_datetime.desc(), Payment.id_payment)
    )
    result: Result = await session.execute(stmt)
    book_ids = result.scalars().all()
    return list(book_ids)


async def get_order_ids_by_user(session: AsyncSession, id_user: int) -> List[int]:
    """
    Get a list of order IDs by the user.
    """

    stmt = (
        select(Order.id_order)
        .where(Order.id_user == id_user)
        .order_by(Order.order_datetime.desc(), Order.id_order)
    )
    result: Result = await session.execute(stmt)
    order_ids = result.scalars().all()
    return list(order_ids)


async def update_user(
    session: AsyncSession, user: User, user_update_data: UserUpdate
) -> UserSchema:
    """
    Update user information.
    """

    if user_update_data.referrer_id is not None:
        referrer = await get_user_by_id(session, user_update_data.referrer_id)
        if referrer is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Referrer with ID {user_update_data.referrer_id} does not exist!!",
            )

    if user_update_data.referrer_id == user.id_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user cannot refer themselves: 'referrer_id' must not equal 'id_user'!!",
        )

    for name, value in user_update_data.model_dump(exclude_unset=True).items():
        setattr(user, name, value)
    await session.commit()

    return await get_user_details(session, id_user=user.id_user)
