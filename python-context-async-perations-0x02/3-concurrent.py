#!/usr/bin/python3
"""
This script demonstrates running multiple database queries concurrently
using asyncio and aiosqlite.
"""

import asyncio
import aiosqlite  # Async version of sqlite3
import time
import os
import sqlite3     # Using synchronous sqlite3 just for setup

# We will use the database created in the previous tasks
DB_FILE = "user_database.db"

# --- Setup Function (Synchronous) ---
def setup_database(db_name):
    """
    A helper function to ensure the database and table exist.
    (Using synchronous sqlite3 for simple setup).
    """
    if os.path.exists(db_name):
        print("Database file already exists.")
        return # Don't re-create if it's already there

    print(f"--- Setting up '{db_name}' for the test ---")
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER
        )
        """)
        sample_users = [('Alice', 30), ('Bob', 25), ('Charlie', 42), ('Dave', 50)]
        cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", sample_users)
        conn.commit()
        print("Database setup complete. 4 users inserted.")
    except sqlite3.Error as e:
        print(f"Error during setup: {e}")
    finally:
        if conn:
            conn.close()

# --- Asynchronous Functions ---

async def async_fetch_users():
    """
    Asynchronously fetches all users from the database.
    """
    print("Task 1: Starting to fetch all users...")
    await asyncio.sleep(0.5) # Simulate network delay
    
    # 'aiosqlite.connect' is an async operation
    async with aiosqlite.connect(DB_FILE) as conn:
        # 'conn.execute' is an async operation
        async with conn.execute("SELECT * FROM users") as cursor:
            # 'cursor.fetchall' is an async operation
            results = await cursor.fetchall()
            
    print("Task 1: Finished fetching all users.")
    return results

async def async_fetch_older_users():
    """
    Asynchronously fetches users older than 40.
    """
    print("Task 2: Starting to fetch users older than 40...")
    await asyncio.sleep(0.5) # Simulate network delay
    
    async with aiosqlite.connect(DB_FILE) as conn:
        async with conn.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            
    print("Task 2: Finished fetching users older than 40.")
    return results

async def fetch_concurrently():
    """
    The main asynchronous function that runs both queries
    concurrently using asyncio.gather.
    """
    print("--- Starting concurrent execution ---")
    start_time = time.time()
    
    # This is the key: asyncio.gather()
    # It takes multiple "awaitable" tasks and runs them at the same time.
    # It waits for all of them to finish before returning.
    all_users_task = async_fetch_users()
    older_users_task = async_fetch_older_users()
    
    # 'results' will be a list: [result_from_task_1, result_from_task_2]
    results = await asyncio.gather(
        all_users_task,
        older_users_task
    )
    
    end_time = time.time()
    print(f"--- Concurrent execution finished in {end_time - start_time:.2f} seconds ---")

    # Unpack the results
    all_users = results[0]
    older_users = results[1]

    print("\nResults from Task 1 (All Users):")
    for user in all_users:
        print(f"  - {user}")
        
    print("\nResults from Task 2 (Users older than 40):")
    for user in older_users:
        print(f"  - {user}")


# --- Main Execution ---
if __name__ == "__main__":
    
    # 1. Run the synchronous setup function first
    setup_database(DB_FILE)

    # 2. Use asyncio.run() to start the main async function
    # This creates the event loop, runs the function, and
    # closes the loop when it's done.
    print("\n--- Starting Asynchronous Database Operations ---")
    try:
        asyncio.run(fetch_concurrently())
    except Exception as e:
        print(f"An error occurred during async execution: {e}")

```

---

### Commit Message

Here is the commit message for this new file.

```bash
feat: Implement concurrent async queries with asyncio.gather
