#!/usr/bin/python3
"""
This module defines a decorator that caches the results
of database queries to avoid redundant calls.
"""

import time
import sqlite3
import functools
import os

DB_FILE = "users.db"
query_cache = {}

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
# We provide this helper decorator, as it is required by the prompt.
def with_db_connection(original_function):
    """
    Decorator to automatically handle database connection and closing.
    """
    @functools.wraps(original_function)
    def wrapper_function(*args, **kwargs):
        """Wrapper that manages the connection."""
        conn = None
        try:
            conn = sqlite3.connect(DB_FILE)
            # Pass the connection 'conn' as the first positional argument
            # to the *next* wrapped function (the cache wrapper)
            result = original_function(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"[DB_CONN] Database error: {e}")
            raise # Re-raise the error
        finally:
            if conn:
                conn.close()
                
    return wrapper_function


# --- Decorator 2: The Cache Logic (Your Task) ---
def cache_query(original_function):
    """
    This is the cache decorator.
    It takes the function to wrap (e.g., fetch_users_with_cache)
    """
    @functools.wraps(original_function)
    def wrapper(*args, **kwargs):
        """
        This is the final wrapper. It contains the cache logic.
        
        - *args will contain the 'conn' object from the decorator above.
        - **kwargs will contain the 'query="..."' argument from the user.
        """
        
        # 1. Get the query string from the keyword arguments.
        # This will be our cache "key".
        query_string = kwargs.get('query')
        
        if not query_string:
            # If no query string was found, we can't cache.
            # Just run the function normally.
            print("[CACHE] No 'query' argument found. Skipping cache.")
            return original_function(*args, **kwargs)

        # 2. Check if the result is already in our cache
        if query_string in query_cache:
            # --- CACHE HIT (FAST) ---
            print(f"[CACHE] Hit! Returning cached result for: {query_string}")
            return query_cache[query_string]
        
        else:
            # --- CACHE MISS (SLOW) ---
            print(f"[CACHE] Miss. Running query and caching result for: {query_string}")
            
            # 3. Run the original function (which hits the database)
            # We must pass all *args (the 'conn') and **kwargs (the 'query')
            result = original_function(*args, **kwargs)
            
            # 4. Save the result in our cache for next time
            query_cache[query_string] = result
            
            # 5. Return the result
            return result
            
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches users. This function is wrapped by both decorators.
    The database will only be hit the first time this is called
    with a unique query.
    """
    print("... (Simulating database work)...")
    time.sleep(1) # Simulate a slow query
    
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("... (Finished database work)...")
    return results

# --- Main Execution ---
if __name__ == "__main__":
    
    # 1. Set up the database
    setup_database()
    
    print("\n--- 1. First Call (Should be SLOW and hit the database) ---")
    start_time = time.time()
    users = fetch_users_with_cache(query="SELECT * FROM users")
    end_time = time.time()
    
    print(f"Results: {users}")
    print(f"Time taken: {end_time - start_time:.2f} seconds\n")

    
    print("\n--- 2. Second Call (Should be INSTANT and use the cache) ---")
    start_time = time.time()
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    end_time = time.time()
    
    print(f"Results: {users_again}")
    print(f"Time taken: {end_time - start_time:.2f} seconds\n")

    print("\n--- 3. Third Call (Different query, should be SLOW) ---")
    start_time = time.time()
    alice = fetch_users_with_cache(query="SELECT * FROM users WHERE name = 'Alice Smith'")
    end_time = time.time()
    
    print(f"Results: {alice}")
    print(f"Time taken: {end_time - start_time:.2f} seconds\n")