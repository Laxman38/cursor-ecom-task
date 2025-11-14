from __future__ import annotations

import sqlite3
from typing import Iterable, Sequence


def _print_table(headers: Sequence[str], rows: Iterable[sqlite3.Row]) -> None:
    rows = list(rows)
    if not rows:
        print("No rows returned.\n")
        return

    column_widths = [len(header) for header in headers]
    for row in rows:
        for idx, header in enumerate(headers):
            column_widths[idx] = max(column_widths[idx], len(str(row[header])))

    def fmt_row(values: Sequence[str]) -> str:
        return " | ".join(
            str(value).ljust(column_widths[idx]) for idx, value in enumerate(values)
        )

    print(fmt_row(headers))
    print("-+-".join("-" * width for width in column_widths))
    for row in rows:
        print(fmt_row([row[header] for header in headers]))
    print()


def run_sample_queries(conn: sqlite3.Connection) -> None:
    queries = [
        (
            "Top 5 Customers by Spend",
            """
            SELECT
                u.user_id,
                u.first_name || ' ' || u.last_name AS customer_name,
                ROUND(SUM(o.total_amount), 2) AS total_spent,
                COUNT(o.order_id) AS order_count
            FROM users u
            JOIN orders o ON o.user_id = u.user_id
            GROUP BY u.user_id, customer_name
            ORDER BY total_spent DESC
            LIMIT 5;
            """,
            ["user_id", "customer_name", "total_spent", "order_count"],
        ),
        (
            "Best Reviewed Products",
            """
            SELECT
                p.product_id,
                p.name AS product_name,
                ROUND(AVG(r.rating), 2) AS avg_rating,
                COUNT(r.review_id) AS review_count
            FROM products p
            JOIN reviews r ON r.product_id = p.product_id
            GROUP BY p.product_id, product_name
            HAVING review_count >= 2
            ORDER BY avg_rating DESC, review_count DESC
            LIMIT 5;
            """,
            ["product_id", "product_name", "avg_rating", "review_count"],
        ),
        (
            "Recent Order Overview",
            """
            SELECT
                o.order_id,
                o.order_date,
                u.first_name || ' ' || u.last_name AS customer_name,
                COUNT(oi.order_item_id) AS item_count,
                ROUND(o.total_amount, 2) AS order_total,
                o.status
            FROM orders o
            JOIN users u ON u.user_id = o.user_id
            JOIN order_items oi ON oi.order_id = o.order_id
            WHERE o.status != 'CANCELLED'
            GROUP BY o.order_id, o.order_date, customer_name, o.total_amount, o.status
            ORDER BY o.order_date DESC
            LIMIT 10;
            """,
            ["order_id", "order_date", "customer_name", "item_count", "order_total", "status"],
        ),
    ]

    for title, sql, headers in queries:
        print(f"=== {title} ===")
        cursor = conn.execute(sql)
        _print_table(headers, cursor.fetchall())


