from __future__ import annotations

import csv
import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List

SCHEMA = """
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    signup_date TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    inventory INTEGER NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    line_total REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    review_date TEXT NOT NULL,
    comment TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
"""


CASTERS: Dict[str, Dict[str, callable]] = {
    "users": {
        "user_id": int,
    },
    "products": {
        "product_id": int,
        "price": float,
        "inventory": int,
    },
    "orders": {
        "order_id": int,
        "user_id": int,
        "total_amount": float,
    },
    "order_items": {
        "order_item_id": int,
        "order_id": int,
        "product_id": int,
        "quantity": int,
        "unit_price": float,
        "line_total": float,
    },
    "reviews": {
        "review_id": int,
        "user_id": int,
        "product_id": int,
        "rating": int,
    },
}


def get_connection(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def load_csv_into_table(conn: sqlite3.Connection, table_name: str, csv_path: Path) -> int:
    with csv_path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = []
        casters = CASTERS.get(table_name, {})
        fieldnames = reader.fieldnames or []
        placeholders = ", ".join("?" for _ in fieldnames)
        columns_clause = ", ".join(fieldnames)

        for row in reader:
            casted_row = [
                casters.get(field, lambda value: value)(row[field])
                for field in fieldnames
            ]
            rows.append(tuple(casted_row))

    if not rows:
        return 0

    conn.executemany(
        f"INSERT INTO {table_name} ({columns_clause}) VALUES ({placeholders})",
        rows,
    )
    conn.commit()
    return len(rows)


def load_all_from_csv(conn: sqlite3.Connection, table_to_csv: Dict[str, Path]) -> Dict[str, int]:
    counts = {}
    for table, csv_path in table_to_csv.items():
        counts[table] = load_csv_into_table(conn, table, csv_path)
    return counts


