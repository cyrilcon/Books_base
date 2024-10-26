"""Create tables

Revision ID: 264ce9af47df
Revises: 
Create Date: 2024-10-23 21:08:23.818312

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "264ce9af47df"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "article",
        sa.Column("id_article", sa.Integer(), nullable=False),
        sa.Column("link", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("language_code", sa.String(length=3), nullable=False),
        sa.Column(
            "added_datetime",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id_article"),
        sa.UniqueConstraint("link"),
    )
    op.create_table(
        "author",
        sa.Column("id_author", sa.Integer(), nullable=False),
        sa.Column("author_name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id_author"),
        sa.UniqueConstraint("author_name"),
    )
    op.create_table(
        "book",
        sa.Column("id_book", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("cover", sa.String(length=255), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column(
            "added_datetime",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id_book"),
        sa.UniqueConstraint("cover"),
    )
    op.create_index(op.f("ix_book_title"), "book", ["title"], unique=False)
    op.create_table(
        "file",
        sa.Column("id_file", sa.Integer(), nullable=False),
        sa.Column("format", sa.String(length=10), nullable=False),
        sa.Column("file_token", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id_file"),
        sa.UniqueConstraint("file_token"),
    )
    op.create_table(
        "genre",
        sa.Column("id_genre", sa.Integer(), nullable=False),
        sa.Column("genre_name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id_genre"),
        sa.UniqueConstraint("genre_name"),
    )
    op.create_table(
        "user",
        sa.Column("id_user", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("full_name", sa.String(length=225), nullable=True),
        sa.Column("username", sa.String(length=32), nullable=True),
        sa.Column("language_code", sa.String(length=3), nullable=False),
        sa.Column(
            "registration_datetime",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "last_activity_datetime",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("base_balance", sa.Integer(), server_default="0", nullable=False),
        sa.PrimaryKeyConstraint("id_user"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_user_full_name"), "user", ["full_name"], unique=False)
    op.create_table(
        "admin",
        sa.Column("id_user", sa.BIGINT(), nullable=False),
        sa.Column(
            "added_datetime",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["user.id_user"],
        ),
        sa.PrimaryKeyConstraint("id_user"),
    )
    op.create_table(
        "blacklist",
        sa.Column("id_user", sa.BIGINT(), nullable=False),
        sa.Column(
            "added_datetime",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["user.id_user"],
        ),
        sa.PrimaryKeyConstraint("id_user"),
    )
    op.create_table(
        "book_author",
        sa.Column("id_book", sa.Integer(), nullable=False),
        sa.Column("id_author", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_author"],
            ["author.id_author"],
        ),
        sa.ForeignKeyConstraint(
            ["id_book"],
            ["book.id_book"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id_book", "id_author"),
    )
    op.create_table(
        "book_file",
        sa.Column("id_book", sa.Integer(), nullable=False),
        sa.Column("id_file", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_book"],
            ["book.id_book"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["id_file"],
            ["file.id_file"],
        ),
        sa.PrimaryKeyConstraint("id_book", "id_file"),
    )
    op.create_table(
        "book_genre",
        sa.Column("id_book", sa.Integer(), nullable=False),
        sa.Column("id_genre", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_book"],
            ["book.id_book"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["id_genre"],
            ["genre.id_genre"],
        ),
        sa.PrimaryKeyConstraint("id_book", "id_genre"),
    )
    op.create_table(
        "discount",
        sa.Column("id_user", sa.BIGINT(), nullable=False),
        sa.Column("discount_value", sa.Integer(), nullable=False),
        sa.Column(
            "received_datetime",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["user.id_user"],
        ),
        sa.PrimaryKeyConstraint("id_user"),
    )
    op.create_table(
        "order",
        sa.Column("id_order", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("id_user", sa.BIGINT(), nullable=False),
        sa.Column("book_title", sa.String(length=255), nullable=False),
        sa.Column("author_name", sa.String(length=255), nullable=False),
        sa.Column(
            "order_datetime",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["user.id_user"],
        ),
        sa.PrimaryKeyConstraint("id_order"),
    )
    op.create_table(
        "payment",
        sa.Column("id_payment", sa.String(length=255), nullable=False),
        sa.Column("id_user", sa.BIGINT(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column(
            "payment_datetime",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["user.id_user"],
        ),
        sa.PrimaryKeyConstraint("id_payment"),
    )
    op.create_table(
        "book_payment",
        sa.Column("id_book", sa.Integer(), nullable=False),
        sa.Column("id_payment", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_book"],
            ["book.id_book"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["id_payment"],
            ["payment.id_payment"],
        ),
        sa.PrimaryKeyConstraint("id_book", "id_payment"),
    )
    op.create_table(
        "premium",
        sa.Column("id_user", sa.BIGINT(), nullable=False),
        sa.Column("id_payment", sa.String(length=255), nullable=True),
        sa.Column(
            "received_datetime",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id_payment"],
            ["payment.id_payment"],
        ),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["user.id_user"],
        ),
        sa.PrimaryKeyConstraint("id_user"),
    )


def downgrade() -> None:
    op.drop_table("premium")
    op.drop_table("book_payment")
    op.drop_table("payment")
    op.drop_table("order")
    op.drop_table("discount")
    op.drop_table("book_genre")
    op.drop_table("book_file")
    op.drop_table("book_author")
    op.drop_table("blacklist")
    op.drop_table("admin")
    op.drop_index(op.f("ix_user_full_name"), table_name="user")
    op.drop_table("user")
    op.drop_table("genre")
    op.drop_table("file")
    op.drop_index(op.f("ix_book_title"), table_name="book")
    op.drop_table("book")
    op.drop_table("author")
    op.drop_table("article")
