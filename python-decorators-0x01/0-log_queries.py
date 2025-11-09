#!/usr/bin/python3
"""
This module defines a decorator to log SQL queries.
"""

import sqlite3
import functools
import os

DB_FILE = "users.db"

# --- Helper function to set up the database ---
def setup_database():
    """
    Creates a simple 'users.db' SQLite database and a 'users' table
    with some sample data. This is REQUIRED for the script to run.
    """
    # Clean up old db file if it exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    print(f"Setting up new database: {DB_FILE}")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    """)
    
    # Insert sample data
    sample_users = [
        ('Alice Smith', 'alice@example.com'),
        ('Bob Johnson', 'bob@example.com')
    ]
    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", sample_users)
    
    conn.commit()
    conn.close()
    print("Database setup complete.")


#### decorator to log SQL queries
def log_queries(original_function):
    """
    This is the decorator that logs the query.
    """
    
    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        """
        This wrapper function adds the logging behavior.
        """
        
        # --- YOUR CODE GOES HERE ---
        # The instructions ask to log the query *before* executing.
        # We find the query in 'kwargs' or 'args'.
        
        query_to_log = None
        if 'query' in kwargs:
            query_to_log = kwargs['query']
        elif args:
            query_to_log = args[0]

        if query_to_log:
            print(f"[LOG] Executing query: {query_to_log}")
        else:
            print("[LOG] Executing function, but could not find query argument.")
        
        # Now we call the original function (e.g., fetch_all_users)
        try:
            result = original_function(*args, **kwargs)
            print(f"[LOG] Query finished successfully.")
            return result
        except Exception as e:
            print(f"[LOG] Query failed with error: {e}")
            raise
    
    return wrapper_function


@log_queries
def fetch_all_users(query):
    """
    Fetches all users from the users.db database.
    This is the function being decorated.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    # --- THIS WAS MISSING ---
    conn.close()
    return results

# --- Main Execution (THIS WAS MISSING) ---
if __name__ == "__main__":
    
    # 1. Set up the database first
    setup_database()
    
    print("\n--- Calling the decorated function ---")
    
    # 2. Fetch users while logging the query
    # This is the line from your instructions that was missing.
    users = fetch_all_users(query="SELECT * FROM users")
    
    print("\n--- Results ---")
    if users:
        for user in users:
            print(user)
    else:
        print("No users found.")
```