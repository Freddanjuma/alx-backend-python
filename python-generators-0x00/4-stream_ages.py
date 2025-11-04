#!/usr/bin/python3
"""
This module contains a generator to stream user ages and a function
to calculate the average age in a memory-efficient way.
"""
import mysql.connector
from mysql.connector import Error
import os
from decimal import Decimal

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


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    This function contains the first loop.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if connection is None:
            print("Failed to connect to the database. Aborting.")
            return

        print("Successfully connected. Streaming user ages...")
        # We only select the 'age' column for efficiency
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data;")

        # --- The 1st Loop ---
        # The cursor itself is an iterator, efficiently fetching rows.
        for row in cursor:
            yield row['age'] # Yield only the age value

    except Error as e:
        print(f"Error streaming data: {e}")
    finally:
        # 5. Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")


def calculate_average_age():
    """
    Uses the stream_user_ages generator to calculate the average age
    without loading the entire dataset into memory.
    This function contains the second loop.
    """
    
    # We use Decimal for precision, just like in the database
    total_age = Decimal('0')
    user_count = 0
    
    # Get the generator object
    age_generator = stream_user_ages()

    # --- The 2nd Loop ---
    # This loop pulls one age at a time from the generator
    for age in age_generator:
        total_age += age
        user_count += 1
    # --- End of 2nd Loop ---

    # Calculate the average
    if user_count > 0:
        # Perform precise division
        average_age = total_age / Decimal(user_count)
        # We round to 2 decimal places for a clean print
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found to calculate an average.")


# --- Main Execution ---
if __name__ == "__main__":
    """
    This block will run only when the script is executed directly.
    """
    
    calculate_average_age()
