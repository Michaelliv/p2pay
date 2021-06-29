from databases import Database
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    Float,
    Text,
    Boolean,
)

from common.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)
metadata = MetaData()


# Table for supported payment methods
payment_methods_table = Table(
    "payment_methods",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "guid",
        String(36),  # 36 characters, 16-byte numbers (as hex), hyphenated
        primary_key=True,
        autoincrement=False,
    ),
    Column("name", Text, nullable=False),
)

# Table for supported currencies
# In real world situation code would have been an Enum
currencies_table = Table(
    "currencies",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("code", Text, primary_key=True, unique=True),
    Column("name", Text, nullable=False),
)

# Table for users
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "guid",
        String(36),  # 36 characters, 16-byte numbers (as hex), hyphenated
        primary_key=True,
        autoincrement=False,
        unique=True,
    ),
    Column("first_name", Text, nullable=False),
    Column("last_name", Text, nullable=False),
    Column("email_address", Text, nullable=False),
)

# Table for representing the payments methods available for individual users.
# In a real world situation, we could have either replaced this table with a KV or in contrary, we could have kept this
# table and instead of using a textual 'details' column we could have used a JSON column.
user_payment_methods_table = Table(
    "user_payment_methods",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "user_guid",
        String(36),  # 36 characters, 16-byte numbers (as hex), hyphenated
        index=True,
    ),
    Column(
        "payment_method_guid",
        String(36),  # 36 characters, 16-byte numbers (as hex), hyphenated
        index=True,
    ),
    Column("details", Text),
)

# Table for storing processed payment records
payments_table = Table(
    "payments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "transaction_guid",
        String(36),  # 36 characters, 16-byte numbers (as hex), hyphenated
        index=True,
    ),
    Column(
        "user_guid",  # Source or the transaction
        String(36),  # 36 characters, 16-byte numbers (as hex), hyphenated
        index=True,
    ),
    Column(
        "payee_guid",  # Target of the transaction
        String(36),  # 36 characters, 16-byte numbers (as hex), hyphenated
        index=True,
    ),
    Column("currency", Text, nullable=False),
    Column("amount", Float, nullable=False),
    Column(
        "payment_method",
        String(36),  # 36 characters, 16-byte numbers (as hex), hyphenated
        index=True,
    ),
    Column("timestamp", Text),
    Column("risk_score", Float, server_default=None),
    Column("is_approved", Boolean, server_default=None),
)
