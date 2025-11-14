## Cursor E-Commerce Task

This project generates a synthetic e-commerce dataset, exports it to CSV files, loads those CSVs into a SQLite database, and runs sample analytical SQL queries across the joined tables.

### Project Structure

```
cursor-ecom-task/
├── data/
│   └── csv/               # Generated CSV files
├── db/
│   └── ecommerce.db       # SQLite database (auto-created)
├── src/
│   ├── __init__.py
│   ├── csv_utils.py       # Helpers for writing CSV files
│   ├── data_generation.py # Synthetic data factories
│   ├── query_runner.py    # Example SQL joins/aggregations
│   ├── sqlite_utils.py    # DB schema + CSV ingestion helpers
│   └── main.py            # Orchestrates the full workflow
└── README.md
```

### Quick Start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python src\main.py
```

Running `src\main.py` will:

1. Build synthetic `Users`, `Products`, `Orders`, `OrderItems`, and `Reviews`.
2. Persist each dataset as a CSV under `data\csv`.
3. Create/reset `db\ecommerce.db` and load each CSV into its table.
4. Execute illustrative SQL queries that join multiple tables and print the results.


