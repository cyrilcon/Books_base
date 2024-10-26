from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas import FileCreate, FileUpdate
from database.models import File, Book, BookFile


async def create_file(session: AsyncSession, file_data: FileCreate) -> File:
    """
    Create a new file.
    """

    file = File(**file_data.model_dump())

    try:
        session.add(file)
        await session.commit()
        return file
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Such a file already exists!!",
        )


async def update_book_files(
    session: AsyncSession, book: Book, files_update: list[FileUpdate]
):
    """
    Update the files related to the book.
    """

    current_files = {book_file.file.format: book_file for book_file in book.files}

    for file_data in files_update:
        file_create_data = FileCreate(**file_data.model_dump())
        if file_data.format in current_files:
            existing_file = current_files[file_data.format].file
            existing_file.file_token = file_data.file_token
        else:
            new_file = await create_file(session, file_create_data)
            book_file = BookFile(file=new_file, book=book)
            session.add(book_file)

    await session.commit()
