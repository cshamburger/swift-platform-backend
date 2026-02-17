import psycopg2
from config import Config

def get_db_connection():
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn

if __name__ == "__main__":
    try:
        conn = get_db_connection()
        print("Database connected successfully!")
        conn.close()
    except Exception as e:
        print("Database connection failed:")
        print(e)
