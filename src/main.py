from __future__ import annotations

from pathlib import Path

from data_generation import DataConfig, generate_all_data
from csv_utils import write_table_to_csv
from sqlite_utils import get_connection, initialize_schema, load_all_from_csv
from query_runner import run_sample_queries


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    csv_dir = base_dir / "data" / "csv"
    db_path = base_dir / "db" / "ecommerce.db"

    config = DataConfig()  # Tweak counts here if desired.
    dataset = generate_all_data(config)

    table_to_csv = {
        table_name: write_table_to_csv(table_name, payload, csv_dir)
        for table_name, payload in dataset.items()
    }

    conn = get_connection(db_path)
    try:
        initialize_schema(conn)
        counts = load_all_from_csv(conn, table_to_csv)
        for table, count in counts.items():
            print(f"Loaded {count} rows into {table}")

        run_sample_queries(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()


