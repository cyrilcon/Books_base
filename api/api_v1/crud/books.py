from typing import List

from fastapi import HTTPException, status
from rapidfuzz import process, fuzz
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.api_v1 import crud
from api.api_v1.schemas import (
    AuthorSchema,
    PriceEnum,
    BookCreate,
    BookUpdate,
    BookSchema,
    BookIdTitle,
    BookTitleSimilarityResult,
    BookTitleSimilarityResponse,
    FileSchema,
    GenreSchema,
    BooksResponse,
    BookResult,
)
from database.models import Book, BookAuthor, BookGenre, BookFile, File


async def _get_book_by_price(session: AsyncSession, price: int) -> Book | None:
    """
    Helper function to get a book by price.
    """

    stmt = select(Book).where(Book.price == price)
    result: Result = await session.execute(stmt)
    book = result.scalar_one_or_none()
    return book


async def _get_book_by_id(session: AsyncSession, id_book: int) -> Book | None:
    """
    Helper function to get a book by ID.
    """

    stmt = (
        select(Book)
        .where(Book.id_book == id_book)
        .options(
            selectinload(Book.authors).joinedload(BookAuthor.author),
            selectinload(Book.genres).joinedload(BookGenre.genre),
            selectinload(Book.files).joinedload(BookFile.file),
        )
    )
    result: Result = await session.execute(stmt)
    book = result.scalar_one_or_none()
    return book


async def _get_books_by_author_id(session: AsyncSession, id_author: int) -> List[Book]:
    """
    Helper function to get books by author ID.
    """

    stmt = (
        select(Book)
        .join(Book.authors)
        .where(BookAuthor.id_author == id_author)
        .options(
            selectinload(Book.authors).joinedload(BookAuthor.author),
            selectinload(Book.genres).joinedload(BookGenre.genre),
            selectinload(Book.files).joinedload(BookFile.file),
        )
    )
    result: Result = await session.execute(stmt)
    books = result.scalars().all()
    return list(books)


async def _get_books_by_genre_id(session: AsyncSession, id_genre: int) -> List[Book]:
    """
    Helper function to get books by genre ID.
    """

    stmt = (
        select(Book)
        .join(Book.genres)
        .where(BookGenre.id_genre == id_genre)
        .options(
            selectinload(Book.authors).joinedload(BookAuthor.author),
            selectinload(Book.genres).joinedload(BookGenre.genre),
            selectinload(Book.files).joinedload(BookFile.file),
        )
    )
    result: Result = await session.execute(stmt)
    books = result.scalars().all()
    return list(books)


async def _get_all_books_ids_and_titles(
    session: AsyncSession,
) -> List[BookIdTitle] | None:
    """
    Helper function to get all book IDs and titles.
    """

    stmt = select(Book.id_book, Book.title)
    result: Result = await session.execute(stmt)
    books = result.fetchall()
    if not books:
        return None
    return [BookIdTitle(id_book=book.id_book, title=book.title) for book in books]


async def create_book(session: AsyncSession, book_data: BookCreate) -> Book:
    """
    Create a new book.
    """

    session.expunge_all()

    book = Book(
        **book_data.model_dump(
            include={
                "id_book",
                "title",
                "description",
                "cover",
                "price",
                "added_datetime",
            }
        )
    )

    if book_data.price == PriceEnum.FIFTY:
        existing_book = await _get_book_by_price(session, PriceEnum.FIFTY)
        if existing_book:
            existing_book.price = PriceEnum.EIGHTY_FIVE
            await session.commit()

    try:
        session.add(book)
        await session.commit()
        return book

    except IntegrityError as e:
        await session.rollback()
        if "id_book" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Book with ID {book.id_book} already exists!!",
            )
        elif "cover" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Such a cover already exists!!",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conflict in book data!!",
            )


async def create_book_details(
    session: AsyncSession, book_data: BookCreate
) -> BookSchema:
    """
    Create a new book with details.
    """

    await create_book(session, book_data=book_data)

    book = await _get_book_by_id(session, id_book=book_data.id_book)

    for author_data in book_data.authors:
        author = await crud.authors.create_author(session, author_data=author_data)
        book.authors.append(BookAuthor(id_book=book_data.id_book, author=author))

    for genre_data in book_data.genres:
        genre = await crud.genres.create_genre(session, genre_data=genre_data)
        book.genres.append(BookGenre(id_book=book_data.id_book, genre=genre))

    for file_data in book_data.files:
        file = await crud.files.create_file(session, file_data=file_data)
        book.files.append(BookFile(id_book=book_data.id_book, file=file))

    await session.commit()

    return await get_book_details(session, id_book=book_data.id_book)


async def get_books_by_author_id(
    session: AsyncSession,
    id_author: int,
    max_results: int,
    page: int | None,
) -> BooksResponse:
    """
    Get books by author ID.
    """

    author = await crud.authors.get_author_by_id(session=session, id_author=id_author)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with ID {id_author} not found!!",
        )

    books = await _get_books_by_author_id(session=session, id_author=id_author)
    books_count = len(books)

    full_books = []
    for book in books:
        book_details = await get_book_details(session, id_book=book.id_book)
        if book_details:
            full_books.append(book_details)

    if page:
        start = (page - 1) * max_results
        end = start + max_results
        full_books = full_books[start:end]
    else:
        full_books = full_books[:max_results]

    books = [BookResult(book=book) for book in full_books]

    return BooksResponse(count=books_count, books=books)


async def get_books_by_genre_id(
    session: AsyncSession,
    id_genre: int,
    max_results: int,
    page: int | None,
) -> BooksResponse:
    """
    Get books by genre ID.
    """

    genre = await crud.genres.get_genre_by_id(session=session, id_genre=id_genre)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with ID {id_genre} not found!!",
        )

    books = await _get_books_by_genre_id(session=session, id_genre=id_genre)
    books_count = len(books)

    full_books = []
    for book in books:
        book_details = await get_book_details(session, id_book=book.id_book)
        if book_details:
            full_books.append(book_details)

    if page:
        start = (page - 1) * max_results
        end = start + max_results
        full_books = full_books[start:end]
    else:
        full_books = full_books[:max_results]

    books = [BookResult(book=book) for book in full_books]

    return BooksResponse(count=books_count, books=books)


async def get_latest_article(session: AsyncSession) -> int:
    """
    Get the latest article of books.
    """

    stmt = select(Book.id_book).order_by(Book.id_book.desc()).limit(1)
    result: Result = await session.execute(stmt)
    latest_article = result.scalar()
    if latest_article is None:
        return 0
    return latest_article


async def update_book_price(session: AsyncSession) -> BookSchema:
    """
    Update the price of the book with a price of 50 to 85.
    """

    book = await _get_book_by_price(session, PriceEnum.FIFTY)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No book with a price of 50 found!!",
        )

    book.price = PriceEnum.EIGHTY_FIVE

    await session.commit()
    await session.refresh(book)

    return await get_book_details(session, id_book=book.id_book)


async def search_books_by_title_with_similarity(
    session: AsyncSession,
    title: str,
    max_results: int,
    similarity_threshold: int,
    page: int | None,
) -> BookTitleSimilarityResponse:
    """
    Search books by title with Levenshtein distance.
    """

    books = await _get_all_books_ids_and_titles(session=session)
    if not books:
        return BookTitleSimilarityResponse(found=0, books=[])

    title_to_ids = {}
    for book in books:
        if book.title in title_to_ids:
            title_to_ids[book.title].append(book.id_book)
        else:
            title_to_ids[book.title] = [book.id_book]

    titles = [book.title for book in books]

    matching_books = process.extract(
        title,
        titles,
        scorer=fuzz.partial_ratio,
        limit=None,
    )

    matching_books = [
        (match[0], match[1])
        for match in matching_books
        if match[1] >= similarity_threshold
    ]

    found_books_count = len(matching_books)

    matching_ids = []
    for match in matching_books:
        matching_ids.extend(title_to_ids[match[0]])

    if not matching_ids:
        return BookTitleSimilarityResponse(found=0, books=[])

    full_books = []
    for id in matching_ids:
        book_details = await get_book_details(session, id_book=id)
        if book_details:
            full_books.append(book_details)

    search_response_books = [
        BookTitleSimilarityResult(levenshtein_distance=round(match[1], 2), book=book)
        for match, book in zip(matching_books, full_books)
    ]

    if page:
        start = (page - 1) * max_results
        end = start + max_results
        search_response_books = search_response_books[start:end]
    else:
        search_response_books = search_response_books[:max_results]

    return BookTitleSimilarityResponse(
        found=found_books_count, books=search_response_books
    )


async def get_book_by_id(session: AsyncSession, id_book: int) -> Book | None:
    """
    Get a book by ID.
    """

    return await _get_book_by_id(session, id_book=id_book)


async def get_book_details(session: AsyncSession, id_book: int) -> BookSchema | None:
    """
    Get book details by ID.
    """

    book = await _get_book_by_id(session, id_book=id_book)

    if book is None:
        return None

    authors = [
        AuthorSchema(
            id_author=author.author.id_author,
            author_name=author.author.author_name,
        )
        for author in book.authors
    ]
    genres = [
        GenreSchema(
            id_genre=genre.genre.id_genre,
            genre_name=genre.genre.genre_name,
        )
        for genre in book.genres
    ]
    files = [
        FileSchema(
            id_file=file.file.id_file,
            format=file.file.format,
            file_token=file.file.file_token,
        )
        for file in book.files
    ]

    return BookSchema(
        id_book=book.id_book,
        title=book.title,
        cover=book.cover,
        price=book.price,
        description=book.description,
        authors=authors,
        genres=genres,
        files=files,
        added_datetime=book.added_datetime,
    )


async def update_book(
    session: AsyncSession,
    book: Book,
    book_update_data: BookUpdate,
    partial: bool = True,
) -> BookSchema:
    """
    Update book information.
    """

    update_data = book_update_data.model_dump(exclude_unset=partial)
    for field, value in update_data.items():
        if field not in ["authors", "genres", "files"] and value is not None:
            setattr(book, field, value)

    if book_update_data.price == PriceEnum.FIFTY:
        existing_book = await _get_book_by_price(session, PriceEnum.FIFTY)
        if existing_book and existing_book.id_book != book.id_book:
            existing_book.price = PriceEnum.EIGHTY_FIVE
            await session.commit()

    await session.commit()

    book = await _get_book_by_id(session, id_book=book.id_book)

    if book_update_data.authors is not None:
        await crud.authors.update_book_authors(session, book, book_update_data.authors)

    if book_update_data.genres is not None:
        await crud.genres.update_book_genres(session, book, book_update_data.genres)

    if book_update_data.files is not None:
        await crud.files.update_book_files(session, book, book_update_data.files)

    try:
        await session.commit()
        await session.refresh(book)

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error occurred while updating the book!!",
        )

    return await get_book_details(session, id_book=book.id_book)


async def delete_book(session: AsyncSession, book: Book) -> None:
    """
    Delete a book.
    """

    for book_file in book.files:
        await session.delete(book_file.file)

    for book_author in book.authors:
        await session.delete(book_author)

    for book_genre in book.genres:
        await session.delete(book_genre)

    await session.delete(book)
    await session.commit()

    # Checking and deleting authors/genres after deleting a book
    for book_author in book.authors:
        await crud.authors.delete_author_if_unlinked(session, book_author.id_author)

    for book_genre in book.genres:
        await crud.genres.delete_genre_if_unlinked(session, book_genre.id_genre)


async def delete_file(session: AsyncSession, id_book: int, file_format: str) -> None:
    """
    Delete a file of the book by its format.
    """

    stmt = (
        select(BookFile)
        .join(File)
        .where(BookFile.id_book == id_book, File.format == file_format)
    )
    result: Result = await session.execute(stmt)
    book_file = result.scalar_one_or_none()

    if not book_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with format '{file_format}' for book with ID {id_book} not found!!",
        )

    file = await session.get(File, book_file.id_file)

    await session.delete(book_file)
    await session.delete(file)
    await session.commit()
