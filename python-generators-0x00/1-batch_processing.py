#!/usr/bin/python3
"""
This module contains functions to stream and process user data in batches.
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


def stream_users_in_batches(batch_size=5):
    """
    Generator that fetches rows in batches from the user_data table.
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

        print(f"Successfully connected. Streaming users in batches of {batch_size}...")
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        # --- The 1st Loop ---
        while True:
            # 2. Fetch a batch of rows
            batch = cursor.fetchmany(batch_size)
            
            # 3. If the batch is empty, we're done
            if not batch:
                break
            
            # 4. Yield the batch to the caller
            yield batch

    except Error as e:
        print(f"Error streaming data: {e}")
    finally:
        # 5. Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")


def batch_processing(batch_size=5):
    """
    Processes each batch to filter users over the age of 25.
    This function uses two loops.
    """
    print(f"\n--- Starting Batch Processing (filter for age > 25) ---")
    
    # Get the generator object
    batch_generator = stream_users_in_batches(batch_size)
    
    batch_number = 1
    
    # --- The 2nd Loop ---
    for batch in batch_generator:
        print(f"\nProcessing Batch #{batch_number} (raw data):")
        # print(batch) # Uncomment to see the full raw batch
        
        filtered_users = []
        
        # --- The 3rd Loop ---
        for user in batch:
            if user['age'] > 25:
                filtered_users.append(user)
        
        # --- End of 3rd Loop ---
        
        if filtered_users:
            print(f"Users over 25 in this batch:")
            for user in filtered_users:
                print(f"  - {user['name']} (Age: {user['age']})")
        else:
            print("No users over 25 in this batch.")
            
        batch_number += 1
    # --- End of 2nd Loop ---
    
    print("\n--- Batch processing complete ---")


# --- Main Execution ---
if __name__ == "__main__":
    """
    This block will run only when the script is executed directly.
    It's here to test and demonstrate the batch_processing() function.
    """
    
    # We can define the batch size here
    processing_batch_size = 3
    batch_processing(processing_batch_size)
