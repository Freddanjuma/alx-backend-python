#!/usr/bin/python3
"""
A decorator that logs SQL queries before executing them.
"""

import sqlite3
import functools
from datetime import datetime


def log_queries(func):
    """Decorator to log SQL queries before execution"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", "")
        # Log the current time and SQL query
        print(f"[{datetime.now()}] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
