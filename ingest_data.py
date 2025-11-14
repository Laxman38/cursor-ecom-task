from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("ecom.db")
DATA_DIR = Path("data")

TABLES = {
    "users": """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL
        );
    """,
    "products": """
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        );
    """,
    "orders": """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total REAL NOT NULL
        );
    """,
    "order_items": """
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        );
    """,
    "reviews": """
        CREATE TABLE reviews (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL
        );
    """,
}


def drop_tables(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    for table in TABLES:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()


def create_tables(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    for sql in TABLES.values():
        cursor.execute(sql)
    conn.commit()


def load_csv_to_table(conn: sqlite3.Connection, table: str, csv_path: Path) -> int:
    df = pd.read_csv(csv_path)
    df.to_sql(table, conn, if_exists="append", index=False)
    return len(df)


def main() -> None:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"{DATA_DIR} directory not found. Please run generate_data.py first.")

    conn = sqlite3.connect(DB_PATH)
    try:
        drop_tables(conn)
        create_tables(conn)

        for table in TABLES:
            csv_path = DATA_DIR / f"{table}.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"{csv_path} not found.")
            inserted = load_csv_to_table(conn, table, csv_path)
            print(f"Inserted {inserted} rows into {table}.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()


