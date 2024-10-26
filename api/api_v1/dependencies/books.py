from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from database import db_helper
from database.models import Book


async def get_book_by_id_depend(
    id_book: Annotated[int, Path(description="Unique book identifier")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Book:
    """
    Get a book by ID.
    """

    book = await crud.books.get_book_by_id(session=session, id_book=id_book)
    if book:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {id_book} not found!!",
    )
