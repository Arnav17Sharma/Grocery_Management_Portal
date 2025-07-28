import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

__cnx = None

def get_sql_connection():
    global __cnx
    # Check if the connection object exists and if it is still connected
    if __cnx is None or not __cnx.is_connected():
        print("Connecting to database...") # Optional: for debugging
        __cnx = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME")
        )
    return __cnx