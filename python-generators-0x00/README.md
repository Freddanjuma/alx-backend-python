Project: Python Generators — Database Seeding and Streaming
📘 Overview

This project demonstrates advanced use of Python generators to stream data efficiently from a MySQL database. It also includes database setup, seeding, and connection logic using mysql.connector.

The goal is to minimize memory usage while working with large datasets — a common requirement in real-world backend systems.

🧩 Features

Connects to a MySQL server and creates a new database (ALX_prodev) if not present.

Creates a user_data table with:

user_id (UUID, Primary Key, Indexed)

name (VARCHAR, NOT NULL)

email (VARCHAR, NOT NULL)

age (DECIMAL, NOT NULL)

Seeds the database using a CSV file (user_data.csv).

Streams data rows one by one using a Python generator — improving performance and memory efficiency.

⚙️ File Structure
alx-backend-python/
└── python-generators-0x00/
    ├── seed.py                # Handles DB creation, table setup, and data insertion
    ├── 0-main.py              # Entry point for running and testing seeding and streaming
    ├── user_data.csv          # Sample user dataset
    ├── README.md              # Documentation file

🧰 Prototypes
def connect_db():
    """Connects to the MySQL database server."""

def create_database(connection):
    """Creates the database 'ALX_prodev' if it does not exist."""

def connect_to_prodev():
    """Connects to the 'ALX_prodev' database."""

def create_table(connection):
    """Creates the 'user_data' table if it does not exist."""

def insert_data(connection, data):
    """Inserts data from 'user_data.csv' into the database."""

def stream_user_data(connection):
    """Generator function to stream user data row by row."""

🚀 How to Run the Project
1️⃣ Install Dependencies
pip install mysql-connector-python

2️⃣ Run the Seeding Script
python 0-main.py


Expected output:

Successfully connected to MySQL server.
Database 'ALX_prodev' created or already exists.
connection successful
Database ALX_prodev is present
[('UUID', 'Name', 'Email', Decimal('Age')), ...]
Streaming rows using generator...

🧪 Testing the Generator

In 0-main.py, rows are streamed using:

for row in seed.stream_user_data(connection):
    print(row)


This ensures only one row is loaded in memory at a time — useful for large-scale datasets.

🧠 Key Concepts

Generator functions (yield) — Efficiently handle large data without loading everything into memory.

MySQL integration — Real-world backend connection and data management.

Data streaming — Essential for APIs, analytics pipelines, and microservices.

🧾 Author

Name: Fred Danjuma
Cohort: ALX Backend Engineering
Repository: alx-backend-python