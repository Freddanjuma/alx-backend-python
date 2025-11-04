#!/usr/bin/python3
"""
This module contains a generator function to stream user data from a database.
"""
import mysql.connector
from mysql.connector import Error
import os

# --- Database Configuration ---
# Read from environment variables for security
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = 'ALX_prodev'


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
        return None
    
    return connection


def stream_users():
    """
    Generator that streams user_data rows one by one.
    This function uses 'yield' and has only one loop.
    """
    connection = None
    cursor = None
    try:
        # 1. Connect to the database
        connection = connect_to_prodev()
        if connection is None:
            print("Failed to connect to the database. Aborting.")
            return

        # 2. Create a cursor
        # dictionary=True returns rows as dictionaries (e.g., row['name'])
        cursor = connection.cursor(dictionary=True)

        # 3. Execute the query
        cursor.execute("SELECT * FROM user_data;")

        # 4. The single loop that yields rows one by one
        # The cursor itself is an iterator, so this is very efficient.
        for row in cursor:
            yield row

    except Error as e:
        print(f"Error streaming data: {e}")
    finally:
        # 5. Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")


# --- Main Execution ---
if __name__ == "__main__":
    """
    This block will run only when the script is executed directly.
    It's here to test and demonstrate the stream_users() generator.
    """
    
    print("Starting user data stream...\n")
    
    # Get the generator object
    user_stream = stream_users()
    
    # Iterate over the generator
    for user in user_stream:
        print(user)
        # You can see it's streaming one by one
        # import time
        # time.sleep(0.5)

    print("\nStream complete.")
