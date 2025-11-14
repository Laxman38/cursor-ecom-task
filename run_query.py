from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("ecom.db")

QUERY = """
SELECT
    u.name AS user_name,
    p.name AS product_name,
    oi.quantity,
    p.price,
    ROUND(oi.quantity * p.price, 2) AS total_amount,
    o.order_date
FROM users u
JOIN orders o ON o.user_id = u.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
ORDER BY o.order_date DESC
LIMIT 10;
"""


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError("ecom.db not found. Run ingest_data.py first.")

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(QUERY, conn)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()


