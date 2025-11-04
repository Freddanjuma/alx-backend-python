#!/usr/bin/python3
"""
This script defines a class-based context manager for handling
database connections automatically.
"""

import sqlite3
import os

DB_FILE = "user_database.db"

class DatabaseConnection:
    """
    A class-based context manager for handling database connections.
    
    This class automatically opens a connection when entering a 'with'
    statement and ensures the connection is properly closed when exiting,
    handling commits and rollbacks based on whether an exception occurred.
    """
    
    def __init__(self, db_name):
        """
        Initializes the context manager with the database name.
        """
        self.db_name = db_name
        self.conn = None
        print(f"Context Manager initialized for database: {self.db_name}")

    def __enter__(self):
        """
        Opens the database connection when entering the 'with' block.
        This is the "setup" part.
        """
        print("Connecting to database...")
        try:
            self.conn = sqlite3.connect(self.db_name)
            # Return the connection object so it can be used
            # in the 'with' block (e.g., 'as conn:')
            return self.conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise  # Re-raise the exception

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the database connection when exiting the 'with' block.
        This is the "teardown" or "cleanup" part.
        
        exc_type, exc_value, traceback will be None if no error
        occurred. If an error happened, they will be populated.
        """
        if self.conn:
            try:
                if exc_type is not None:
                    # An error occurred inside the 'with' block
                    print(f"An error occurred: {exc_value}. Rolling back changes.")
                    self.conn.rollback()
                else:
                    # No error occurred, commit the changes
                    print("No errors. Committing changes.")
                    self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error during __exit__: {e}")
            finally:
                # This ALWAYS runs, ensuring the connection is closed.
                print("Closing database connection.")
                self.conn.close()
        
        # Return False (or None) to re-raise any exception that occurred.
        # If we returned True, the exception would be suppressed.
        return False


def setup_database(db_name):
    """
    A helper function to create and populate the database
    so the 'SELECT' query has data to work with.
    """
    print(f"--- Setting up '{db_name}' for the test ---")
    if os.path.exists(db_name):
        os.remove(db_name)
        
    try:
        # Use a *normal* connection to set up the table
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create the users table
        cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER
        )
        """)
        
        # Insert sample data
        sample_users = [
            ('Alice', 30),
            ('Bob', 25),
            ('Charlie', 42)
        ]
        cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", sample_users)
        
        conn.commit()
        print("Database setup complete. 3 users inserted.")
    except sqlite3.Error as e:
        print(f"Error during setup: {e}")
    finally:
        if conn:
            conn.close()


# --- Main Execution ---
if __name__ == "__main__":
    
    # 1. Run the setup to create the DB and table
    setup_database(DB_FILE)

    print("\n--- Testing the DatabaseConnection Context Manager ---")
    
    try:
        # 2. Use the context manager as per the instructions
        with DatabaseConnection(DB_FILE) as conn:
            
            # 'conn' is the connection object returned by __enter__
            cursor = conn.cursor()
            
            # 3. Perform the query
            print("\nInside 'with' block: Executing 'SELECT * FROM users'")
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            
            # 4. Print the results
            print("Query successful. Fetched users:")
            for user in results:
                print(f"  - {user}")

        # 5. The __exit__ method is automatically called here.
        #    You will see "Committing changes." and "Closing database."
        #    printed right after this block.

    except Exception as e:
        print(f"\nMain script caught an error: {e}")
