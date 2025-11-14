# 🚀 Cursor AI Prompts Used in This Project

This project was developed using an AI-assisted workflow in **Cursor**, following a modular A-SDLC (AI-Software Development Life Cycle) approach.  
Below are the exact prompts used for each stage of the project.

---

## 🧱 Prompt 1 — Project Setup & Structure

**Prompt:**

Create the basic structure of a Python project named `cursor-ecom-task`.  
The goal is to:

1. Generate synthetic e-commerce data  
2. Store the data as CSV files  
3. Load the CSVs into a SQLite database  
4. Run SQL join queries and print the output  

Create the following folders and files:

- `/data`  
- `/scripts`  
- `scripts/generate_data.py`  
- `scripts/ingest_data.py`  
- `scripts/run_query.py`  
- `README.md`

Set up the project structure accordingly.

---

## 🧪 Prompt 2 — Generate Synthetic E-Commerce Data

**Prompt:**

Write a complete Python script inside `scripts/generate_data.py` that uses `faker` and `pandas` to generate:

- 100 Users (id, name, email, address)  
- 50 Products (id, name, category, price)  
- 200 Orders (id, user_id, order_date, total)  
- 500 OrderItems (id, order_id, product_id, quantity)  
- 150 Reviews (id, product_id, user_id, rating, comment)

Save each dataset as a separate `.csv` file in the `/data` folder.  
Add clear print statements confirming successful generation.

---

## 🗄️ Prompt 3 — Ingest CSV Files Into SQLite Database

**Prompt:**

Write the full Python script for `scripts/ingest_data.py` that:

- Creates a SQLite database named `ecom.db`
- Creates tables for Users, Products, Orders, OrderItems, and Reviews
- Reads the CSVs from `/data` using `pandas`
- Inserts the data into the respective tables
- Drops tables first if they already exist (idempotent)
- Prints a success message after each table load

Use `sqlite3` for the database connection.

---

## 🧮 Prompt 4 — SQL Join Query + Python Execution Script

**Prompt:**

Write a Python script in `scripts/run_query.py` that:

- Connects to the `ecom.db` SQLite database  
- Executes an SQL query that joins:

  - Users  
  - Orders  
  - OrderItems  
  - Products  

- Output fields:  
  - `user_name`  
  - `product_name`  
  - `quantity`  
  - `price`  
  - `total_amount = price * quantity`  
  - `order_date`

- Limit result to 10 rows  
- Print the result as a `pandas` DataFrame in a well-formatted manner

---

## 🚀 Prompt 5 — GitHub Repository Setup

**Prompt:**

Generate the Git commands to:

- Initialize a git repository  
- Add all files  
- Commit changes  
- Create the `main` branch  
- Add remote origin for the GitHub repo `cursor-ecom-task`  
- Push all code to GitHub  

Provide the exact commands.

---

# ✅ End of Prompts
These prompts were executed sequentially in Cursor to complete the project within a 30-minute AI-assisted development window.
