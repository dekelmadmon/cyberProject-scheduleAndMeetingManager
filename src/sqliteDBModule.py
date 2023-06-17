import sqlite3
import os


class Database:
    def __init__(self):
        """Initialize database connection and create Data table if it doesn't exist"""
        self.database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'SQLite_Python.db'))
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.database_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        try:
            with self.connection:
                sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS Data (
                                                id INTEGER PRIMARY KEY,
                                                username TEXT,
                                                userEmail TEXT NOT NULL UNIQUE,
                                                userPassword TEXT NOT NULL,
                                                userActivity TEXT,
                                                activityDate TEXT,
                                                startPoint REAL,
                                                duration REAL);'''
                self.cursor.execute(sqlite_create_table_query)
                sqlite_select_query = "SELECT sqlite_version();"
                self.cursor.execute(sqlite_select_query)
                record = self.cursor.fetchone()
                print("SQLite Database Version is: ", record)
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            self.reset_database()

    def disconnect(self):
        self.connection.close()

    def reset_database(self):
        """
        Delete the existing SQLite database file and create a new one.
        """
        self.disconnect()
        os.remove(self.database_path)
        self.connect()



    def sign_in(self, username, email, password):
        """
        Sign up a new user by inserting their details into the database
        """
        if not self.authenticate_user_credentials(email, password):
            self.create_user(username, email, password)
            return True
        return False

    def authenticate_user_credentials(self, email, password):
        """
        Check if user with given email and password exists in the database
        """
        self.connect()
        query = '''
            SELECT EXISTS (
                SELECT 1 FROM Data
                WHERE userEmail = ? AND userPassword = ?
            )
        '''
        self.cursor.execute(query, (email, password))
        result = bool(self.cursor.fetchone()[0])
        self.disconnect()
        return result

    def user_exists(self, email):
        """
        Check if a user exists in the database based on their email address
        """
        self.connect()
        sqlite_check_user = '''SELECT COUNT(*) FROM Data WHERE userEmail = ?'''
        sqlite_check_user_args = (email,)
        self.cursor.execute(sqlite_check_user, sqlite_check_user_args)
        count = self.cursor.fetchone()[0]
        self.disconnect()
        return count > 0

    def create_user(self, username, email, password):
        """
        Insert a new user into the database
        """
        if not self.user_exists(email):
            self.connect()
            sqlite_insert_user = '''INSERT INTO Data (username, userEmail, userPassword)
                                       VALUES (?, ?, ?)'''
            sqlite_insert_user_args = (username, email, password)
            self.cursor.execute(sqlite_insert_user, sqlite_insert_user_args)
            self.connection.commit()
            self.disconnect()

    def delete_user(self, email):
        """
        Delete a user from the database based on their email address
        """
        if self.user_exists(email):
            self.connect()
            sqlite_delete_user = '''DELETE FROM Data WHERE userEmail = ?'''
            sqlite_delete_user_args = (email,)
            self.cursor.execute(sqlite_delete_user, sqlite_delete_user_args)
            self.connection.commit()
            self.disconnect()

