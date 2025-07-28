from werkzeug.security import generate_password_hash

def create_user(connection, user_data):
    """Inserts a new user into the database with a hashed password."""
    cursor = connection.cursor()
    
    # Never store plain text passwords. Always hash them first.
    hashed_password = generate_password_hash(user_data['password'])
    
    query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
    data = (user_data['username'], user_data['email'], hashed_password)
    
    try:
        cursor.execute(query, data)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        connection.rollback()
        print(f"Database error: {e}")
        return None

def get_user_by_email(connection, email):
    """Retrieves a user's full record by their email address."""
    # dictionary=True returns rows as dictionaries, which is very convenient
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    return user

def get_user_by_id(connection, user_id):
    """Retrieves a user's full record by their ID. Required for Flask-Login."""
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    return user