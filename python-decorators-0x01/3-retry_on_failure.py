#!/usr/bin/python3
"""
This module defines a decorator that retries a function
if it fails due to a transient error.
"""

import time
import sqlite3
import functools
import os

DB_FILE = "users.db"

# --- Helper function to ensure the database exists ---
def setup_database():
    """
    Checks if the database exists. If not, it creates it.
    This uses the 'users.db' from the previous task.
    """
    if not os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} not found. Running setup...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """)
        sample_users = [
            ('Alice Smith', 'alice@example.com'),
            ('Bob Johnson', 'bob@example.com')
        ]
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", sample_users)
        conn.commit()
        conn.close()
        print("Database setup complete.")
    else:
        print(f"Database {DB_FILE} already exists.")


# --- Decorator 1: Database Connection Handler ---
# The prompt asks us to provide this helper decorator.
def with_db_connection(original_function):
    """
    Decorator to automatically handle database connection and closing.
    It connects, passes the connection 'conn' to the wrapped function,
    and ensures the connection is closed.
    """
    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        """Wrapper that manages the connection."""
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE)
            print(f"[DB_CONN] Connection established.")
            
            # Pass the connection 'conn' as the first argument
            # to the *next* wrapped function (the retry wrapper)
            result = original_function(conn, *args, **kwargs)
            
            return result
            
        except sqlite3.Error as e:
            print(f"[DB_CONN] Database error: {e}")
            raise # Re-raise the error
        finally:
            if conn:
                conn.close()
                print(f"[DB_CONN] Connection closed.")
                
    return wrapper_function


# --- Decorator 2: The Retry Logic (Your Task) ---
def retry_on_failure(retries=3, delay=1):
    """
    This is a DECORATOR FACTORY.
    It takes arguments (retries, delay) and *returns* the
    actual decorator that will wrap the function.
    """
    
    def decorator(original_function):
        """
        This is the actual decorator.
        It takes the function to wrap (e.g., fetch_users_with_retry)
        """
        @functools.wraps(original_function)
        def wrapper(*args, **kwargs):
            """
            This is the final wrapper. It contains the retry loop.
            """
            
            # Loop from 0 to 'retries - 1'
            for attempt in range(retries):
                try:
                    # --- Try to run the original function ---
                    # *args will contain the 'conn' object from the
                    # @with_db_connection decorator.
                    return original_function(*args, **kwargs)
                    
                except Exception as e:
                    # --- This runs if the function fails ---
                    
                    # Log the failure
                    print(f"[RETRY] Attempt {attempt + 1}/{retries} failed: {e}")
                    
                    # If this was the last attempt, give up and
                    # re-raise the exception so the program fails.
                    if attempt + 1 == retries:
                        print(f"[RETRY] All {retries} retry attempts failed.")
                        raise
                    
                    # Wait for 'delay' seconds before the next loop
                    print(f"[RETRY] Waiting {delay} second(s) before retrying...")
                    time.sleep(delay)
                    
        return wrapper
        
    # The factory returns the decorator
    return decorator


# --- We need a global counter to simulate a *transient* error ---
# This will make the function fail the first two times, but
# succeed on the third attempt.
ATTEMPT_COUNTER = 0

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches users. This function is wrapped by both decorators.
    It will fail its first two attempts to simulate a temporary error.
    """
    global ATTEMPT_COUNTER
    ATTEMPT_COUNTER += 1
    
    # --- Error Simulation ---
    if ATTEMPT_COUNTER < 3:
        print(f"--- Simulating failure on attempt {ATTEMPT_COUNTER} ---")
        # Raise a common transient error
        raise sqlite3.OperationalError("Simulating: database is locked")
    # --- End of Simulation ---
    
    print(f"--- Attempt {ATTEMPT_COUNTER}: Simulation success! Fetching data... ---")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# --- Main Execution ---
if __name__ == "__main__":
    
    # 1. Set up the database
    setup_database()
    
    print("\n--- Calling the decorated function with retries ---")
    
    # 2. Attempt to fetch users with automatic retry on failure
    # Note: We call it with no arguments. The @with_db_connection
    # decorator provides the 'conn' argument automatically.
    users = fetch_users_with_retry()
    
    print("\n--- Final Results ---")
    if users:
        print("Successfully fetched users:")
        for user in users:
            print(user)
    else:
        print("No users were fetched.")