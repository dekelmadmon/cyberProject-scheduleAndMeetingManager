import sqlite3
import os


class Database:
    def __init__(self):
        """Initialize database connection and create Data table if it doesn't exist"""
        self.database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'SQLite_Python.db'))
        self.create()

    def connect(self):
        connection = sqlite3.connect(self.database_path, check_same_thread=False)
        #cursor = self.connection.cursor()
        return connection

    def disconnect(self, connection):
        connection.close()

    def reset_database(self):
        """
        Delete the existing SQLite database file and create a new one.
        """
        self.disconnect()
        os.remove(self.database_path)
        self.connect()


    def authenticate_user_credentials(self, email, password):
        """
        Check if user with given email and password exists in the database
        """
        connection = None
        cursor = None
        result = None
        try:
            connection = self.connect()
            cursor = connection.cursor()

            query = '''
                        SELECT EXISTS (
                            SELECT 1 FROM Data
                            WHERE userEmail = ? AND userPassword = ?
                        )
                    '''
            cursor.execute(query, (email, password))
            result = bool(cursor.fetchone()[0])
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if (cursor != None):
                cursor.close()
            if (connection != None):
                self.disconnect(connection)
        return result

    def user_exists(self, email):
        """
        Check if a user exists in the database based on their email address
        """
        connection = None
        cursor = None
        count = None
        try:
            connection = self.connect()
            cursor = connection.cursor()

            query = """
                SELECT COUNT(*) FROM Data WHERE userEmail = ?
                """
            cursor.execute(query, (email, ))
            count = cursor.fetchone()[0]
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if (cursor != None):
                cursor.close()
            if (connection != None):
                self.disconnect(connection)

        return count > 0

    def create_user(self, username, email, password):
        """
        Insert a new user into the database
        """
        if not self.user_exists(email):
            connection = None
            cursor = None
            try:
                connection = self.connect()
                cursor = connection.cursor()

                query = '''INSERT INTO Data (username, userEmail, userPassword)
                                       VALUES (?, ?, ?)'''
                cursor.execute(query, (username, email, password))

                connection.commit()
            except sqlite3.Error as error:
                print("Error while connecting to sqlite", error)
            finally:
                if (cursor != None):
                    cursor.close()
                if (connection != None):
                    self.disconnect(connection)

    def delete_user(self, email):
        """
        Delete a user from the database based on their email address
        """
        if self.user_exists(email):
            connection = None
            cursor = None
            try:
                connection = self.connect()
                cursor = connection.cursor()

                query = '''DELETE FROM Data WHERE userEmail = ?'''
                cursor.execute(query, (email))
            except sqlite3.Error as error:
                print("Error while connecting to sqlite", error)
            finally:
                if (cursor != None):
                    cursor.close()
                if (connection != None):
                    self.disconnect(connection)

    def create(self):
        connection = None
        cursor = None
        try:
            connection = self.connect()
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Data (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    userEmail TEXT NOT NULL UNIQUE,
                    userPassword TEXT NOT NULL
                )
                """
            )

            # Create the client_database table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS client_database (
                    clientemail TEXT PRIMARY KEY,
                    username TEXT,
                    password TEXT
                )
                """
            )

            # Create the meetings table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS meetings (
                    meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    participants TEXT
                )
                """
            )

            # Create the invitations table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS invitations (
                    clientemail TEXT,
                    recipient TEXT,
                    date TEXT,
                    status TEXT,
                    FOREIGN KEY (clientemail) REFERENCES client_database(clientemail)
                )
                """
            )

            # Commit the changes and close the database connection
            connection.commit()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if (cursor != None):
                cursor.close()
            if (connection != None):
                self.disconnect(connection)