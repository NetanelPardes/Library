import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'root',
        database = 'library_db'
    )

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS books(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title varchar(50) NOT NULL,
                    author varchar(50) NOT NULL,
                    genre ENUM('Fiction','Non-Fiction','Science','History','Other'),
                    is_available BOOLEAN DEFAULT FALSE,
                    borrowed_by_member_id INT DEFAULT NULL
                   )
                   """)
    conn.commit()

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS members(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name varchar(50) NOT NULL,
                    email varchar(50) NOT NULL UNIQUE,
                    active_is BOOLEAN DEFAULT TRUE,
                    total_borrows INT DEFAULT 0
                   )
                   """)
    conn.commit()
    cursor.close()
    conn.close()