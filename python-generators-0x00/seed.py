import mysql.connector
from mysql.connector import Error
import os
import csv
import uuid

# --- Database Configuration ---
# Read from environment variables for security
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = 'ALX_prodev'

def connect_db():
    """Connects to the MySQL database server (without specifying a database)."""
    connection = None
    if not DB_USER or not DB_PASS:
        print("Error: DB_USER and DB_PASS environment variables are not set.")
        return None
        
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        if connection.is_connected():
            print("Successfully connected to MySQL server.")
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
    
    return connection

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    if connection is None:
        return
        
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created or already exists.")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if cursor:
            cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database in MYSQL."""
    connection = None
    if not DB_USER or not DB_PASS:
        print("Error: DB_USER and DB_PASS environment variables are not set.")
        return None

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        if connection.is_connected():
            print(f"Successfully connected to database '{DB_NAME}'.")
    except Error as e:
        print(f"Error connecting to database '{DB_NAME}': {e}")
    
    return connection

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    if connection is None:
        return

    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL(3, 0) NOT NULL
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table 'user_data' created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()

def load_data_from_csv(filename):
    """Helper function to load data from the CSV file."""
    data = []
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            try:
                next(reader)  # Skip the header row
            except StopIteration:
                print(f"Error: {filename} is empty or has no header.")
                return []
                
            for row in reader:
                # --- THIS IS THE FIX for Error 1 ---
                # Check if the row is not empty AND has exactly 3 columns
                if row and len(row) == 3:
                    data.append(row)
                elif row:
                    print(f"Skipping malformed row: {row}") # Lets you see the bad data
        
        print(f"Loaded {len(data)} valid data rows from {filename}.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found. Make sure '{filename}' is in the same directory.")
    except Exception as e:
        print(f"Error reading {filename}: {e}")
    return data

def insert_data(connection, csv_file):
    """
    Reads data from a CSV file and inserts it into the database.
    This function now matches the prototype from 0-main.py.
    """
    if connection is None:
        return

    # --- Step 1: Load data from the CSV file ---
    # This now uses the more robust 'load_data_from_csv' function
    data = load_data_from_csv(csv_file)
    if not data:
        print("No valid data loaded from CSV, nothing to insert.")
        return

    # --- Step 2: Insert data into the database ---
    cursor = None
    try:
        cursor = connection.cursor()
        
        check_query = "SELECT user_id FROM user_data WHERE email = %s"
        insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
        
        rows_to_insert = []
        rows_skipped = 0
        
        for row in data:
            name, email, age = row
            # Check if email already exists
            cursor.execute(check_query, (email,))
            if cursor.fetchone() is None:
                # If email not found, add to our list for insertion
                user_id = str(uuid.uuid4())
                rows_to_insert.append((user_id, name, email, int(age)))
            else:
                rows_skipped += 1
        
        # Insert all new rows in a single, efficient operation
        if rows_to_insert:
            cursor.executemany(insert_query, rows_to_insert)
            connection.commit()
            print(f"Successfully inserted {len(rows_to_insert)} new rows.")
        
        if rows_skipped > 0:
            print(f"Skipped {rows_skipped} rows (email already exists).")
            
        if not rows_to_insert and rows_skipped > 0:
            print("All valid data rows were already present in the database.")
            
    except Error as e:
        print(f"Error inserting data: {e}")
    except ValueError as e:
        print(f"Data error: {e}. Check if 'age' is a valid number.")
    finally:
        if cursor:
            cursor.close()

# --- THIS IS THE FIX for Error 2 ---
def stream_user_data(connection):
    """Generator that streams user_data rows one by one."""
    if connection is None:
        print("No database connection.")
        return

    cursor = None
    try:
        # dictionary=True makes the cursor return rows as dictionaries
        # which is what your 0-main.py file expects (e.g., row['name'])
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        
        for row in cursor:
            yield row
            
    except Error as e:
        print(f"Error streaming data: {e}")
    finally:
        if cursor:
            cursor.close()