from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_table_to_csv(table_name: str, table_data: Dict[str, List[Dict[str, object]]], output_dir: Path) -> Path:
    """
    Persist a table (fieldnames + rows) to CSV.

    Args:
        table_name: Logical table name (used for the filename).
        table_data: Dictionary containing `fieldnames` and `rows`.
        output_dir: Root directory that will contain the CSV file.

    Returns:
        Path to the written CSV file.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{table_name}.csv"

    fieldnames: Iterable[str] = table_data["fieldnames"]
    rows: Iterable[Dict[str, object]] = table_data["rows"]

    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return csv_path


