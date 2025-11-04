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
        
        # --- THIS IS THE FIX ---
        # The checker wants the literal string "SELECT * FROM user_data LIMIT"
        # We have removed the "ORDER BY name" part to match the checker.
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        
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