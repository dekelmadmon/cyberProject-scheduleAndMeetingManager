import json
import sqlite3

from src import sqliteDBModule
from src.managers.managerInterface import ManagerInterface


class LoginManager(ManagerInterface):
    def __init__(self):
        self.db = sqliteDBModule.Database()
        print("Init")

    def create(self, data):
        """
        Creates a new user with the provided data if the user does not already exist.
        """
        email = data["email"]
        password = data["password"]
        username = data["username"]
        response = False
        if not self.authenticate_user_credentials(email, password):
            self.create_user(username, email, password)
            response = True

        return json.dumps({'response': response})

    def retrieve(self, data):
        """
        Retrieves user information based on the provided data if the user exists.
        """
        email = data["email"]
        password = data["password"]
        response = False
        if self.authenticate_user_credentials(email, password):
            response = True

        return json.dumps({'response': response})

    def sign_in(self, username, email, password):
        """
        Signs up a new user by inserting their details into the database.
        Returns True if the user is successfully signed up, False otherwise.
        """
        if not self.authenticate_user_credentials(email, password):
            self.create_user(username, email, password)
            return True
        return False

    def authenticate_user_credentials(self, email, password):
        """
        Checks if a user with the given email and password exists in the database.
        Returns True if the user exists, False otherwise.
        """
        connection = None
        cursor = None
        result = None
        try:
            connection = self.db.connect()
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
            if cursor is not None:
                cursor.close()
            if connection is not None:
                self.db.disconnect(connection)
        return result

    def user_exists(self, email):
        """
        Checks if a user exists in the database based on their email address.
        Returns True if the user exists, False otherwise.
        """
        connection = None
        cursor = None
        count = None
        try:
            connection = self.db.connect()
            cursor = connection.cursor()

            query = """
                    SELECT COUNT(*) FROM Data WHERE userEmail = ?
                    """
            cursor.execute(query, (email,))
            count = cursor.fetchone()[0]
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                self.db.disconnect(connection)

        return count > 0

    def create_user(self, username, email, password):
        """
        Inserts a new user into the database.
        """
        if not self.user_exists(email):
            connection = None
            cursor = None
            try:
                connection = self.db.connect()
                cursor = connection.cursor()

                query = '''INSERT INTO Data (username, userEmail, userPassword)
                                       VALUES (?, ?, ?)'''
                cursor.execute(query, (username, email, password))

                connection.commit()
            except sqlite3.Error as error:
                print("Error while connecting to sqlite", error)
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    self.db.disconnect(connection)

    def delete_user(self, email):
        """
        Deletes a user from the database based on their email address.
        """
        if self.user_exists(email):
            connection = None
            cursor = None
            try:
                connection = self.db.connect()
                cursor = connection.cursor()

                query = '''DELETE FROM Data WHERE userEmail = ?'''
                cursor.execute(query, (email,))
            except sqlite3.Error as error:
                print("Error while connecting to sqlite", error)
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None:
                    self.db.disconnect(connection)
