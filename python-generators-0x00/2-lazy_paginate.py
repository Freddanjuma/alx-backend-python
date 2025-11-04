#!/usr/bin/python3
"""
This module contains a generator for lazy-loading paginated user data.
"""
import mysql.connector
from mysql.connector import Error
import os

# --- Database Configuration ---
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = 'ALX_prodev'


def connect_to_prodev():
    """Helper function to connect to the ALX_prodev database."""
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
    except Error as e:
        print(f"Error connecting to database '{DB_NAME}': {e}")
        return None
    
    return connection


def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database using LIMIT and OFFSET.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if connection is None:
            return []  # Connection failed
        
        cursor = connection.cursor(dictionary=True)
        
        # We use ORDER BY to ensure pagination is stable
        query = "SELECT * FROM user_data ORDER BY name LIMIT %s OFFSET %s"
        
        # The tuple (page_size, offset) passes arguments safely
        cursor.execute(query, (page_size, offset))
        
        page_data = cursor.fetchall()
        return page_data
        
    except Error as e:
        print(f"Error paginating data: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def lazy_paginate(page_size):
    """
    Implements the paginate_users function to lazily fetch pages.
    Starts at offset 0 and uses only one loop.
    """
    offset = 0
    
    # This is the single loop required by the instructions
    while True:
        print(f"\n--- [Generator] Fetching page at offset {offset} (page_size={page_size}) ---")
        
        # Call the helper function to get the data
        page = paginate_users(page_size, offset)
        
        # If the page is empty, we have reached the end of the data
        if not page:
            print("--- [Generator] No more data. Stopping generator. ---")
            break
        
        # Yield the entire page (which is a list of users)
        yield page
        
        # Increment the offset for the *next* time the loop runs
        offset += page_size


# --- Main Execution ---
if __name__ == "__main__":
    """
    This block will run only when the script is executed directly.
    It's here to test and demonstrate the lazy_paginate() generator.
    """
    
    print("--- Starting lazy pagination test (page_size = 3) ---")
    
    # 1. Create the generator object.
    #    Note: No database connection is made here.
    page_generator = lazy_paginate(page_size=3)
    
    try:
        # 2. Request the first page
        print("\nRequesting first page...")
        # The database is only queried *now*, when we call next()
        first_page = next(page_generator)
        print(f"Received page 1 with {len(first_page)} users:")
        for user in first_page:
            print(f"  - {user['name']}")
        
        # 3. Request the second page
        print("\nRequesting second page...")
        # The database is queried again *now*
        second_page = next(page_generator)
        print(f"Received page 2 with {len(second_page)} users:")
        for user in second_page:
            print(f"  - {user['name']}")

        # 4. Request all remaining pages with a loop
        print("\nRequesting all remaining pages...")
        page_num = 3
        for page in page_generator:
            print(f"Received page {page_num} with {len(page)} users:")
            for user in page:
                print(f"  - {user['name']}")
            page_num += 1

    except StopIteration:
        # This will be hit if the loop finishes and 'next()' is called again
        print("All pages have been fetched.")
    
    print("\n--- Lazy pagination test complete ---")
