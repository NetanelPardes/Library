import mysql.connector

class DBconnection:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = 'root'
        self.database = 'library_db'
    def get_connection(self):
        return mysql.connector.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            database = self.database
        )

    def create_tables(self):
        conn = self.get_connection()
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
                        is_active BOOLEAN DEFAULT TRUE,
                        total_borrows INT DEFAULT 0
                    )
                    """)
        conn.commit()
        cursor.close()
        conn.close()