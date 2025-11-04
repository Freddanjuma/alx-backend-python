#!/usr/bin/python3
"""
This script defines a reusable class-based context manager
that takes a query and parameters, executes it, and
manages the database connection.
"""

import sqlite3
import os

# We will use the database created in the previous tasks
DB_FILE = "user_database.db"

class ExecuteQuery:
    """
    A class-based context manager that connects to a database,
    executes a given query with parameters, and returns the results.
    
    It automatically handles connection setup, execution, and teardown.
    """
    
    def __init__(self, query, params=()):
        """
        Initializes the context manager with the database name,
        the query to execute, and its parameters.
        """
        self.db_name = DB_FILE
        self.query = query
        self.params = params
        self.conn = None
        print(f"Query Executor initialized for: {self.query}")

    def __enter__(self):
        """
        Opens the database connection, creates a cursor,
        executes the query, fetches the results, and returns them.
        """
        print("Connecting to database and executing query...")
        try:
            self.conn = sqlite3.connect(self.db_name)
            cursor = self.conn.cursor()
            
            # Execute the stored query with the stored parameters
            cursor.execute(self.query, self.params)
            
            # Fetch the results
            results = cursor.fetchall()
            
            # Return the results so they can be used in the 'with' block
            return results
            
        except sqlite3.Error as e:
            print(f"Error during query execution: {e}")
            raise  # Re-raise the exception

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the database connection.
        Handles commit/rollback based on whether an error occurred.
        """
        if self.conn:
            try:
                if exc_type is not None:
                    # An error occurred
                    print(f"An error occurred: {exc_value}. Rolling back.")
                    self.conn.rollback()
                else:
                    # No error, commit (good practice for non-SELECT queries)
                    print("Query successful. Committing.")
                    self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error during __exit__: {e}")
            finally:
                # This ALWAYS runs.
                print("Closing database connection.")
                self.conn.close()
        
        # Return False to re-raise any exception
        return False


# --- Main Execution ---
if __name__ == "__main__":
    
    # Check if the database exists from previous tasks
    if not os.path.exists(DB_FILE):
        print(f"Error: Database file '{DB_FILE}' not found.")
        print("Please run '0-databaseconnection.py' or '1-generator_context_manager.py' first to create it.")
    else:
        # 1. Define the query and parameters as per the instructions
        sql_query = "SELECT * FROM users WHERE age > ?"
        parameters = (25,)  # Must be a tuple!

        print(f"\n--- Testing the ExecuteQuery Context Manager ---")
        print(f"Query: {sql_query}")
        print(f"Params: {parameters}")

        try:
            # 2. Use the context manager
            # The 'results' variable here gets its value
            # from the 'return results' line in __enter__
            with ExecuteQuery(sql_query, parameters) as results:
                
                print("\nQuery executed successfully.")
                print("Users older than 25:")
                
                if results:
                    for user in results:
                        # The users 'Alice' (30), 'Charlie' (42), and 'Dave' (50)
                        # should be printed. 'Bob' (25) should be filtered out.
                        print(f"  - {user}")
                else:
                    print("  No users found matching the criteria.")

        except Exception as e:
            print(f"\nMain script caught an error: {e}")
