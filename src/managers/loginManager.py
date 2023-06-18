import json
import sqlite3

from src import sqliteDBModule
from src.managers.managerInterface import ManagerInterface


class LoginManager(ManagerInterface):
    def __init__(self):
        self.db = sqliteDBModule.Database()
        print("Init")

    def create(self, data):
        email = data["email"]
        password = data["password"]
        username = data["username"]
        response = False
        if not self.authenticate_user_credentials(email, password):
            self.create_user(username, email, password)
            response = True

        return json.dumps({'response': response})
    def retrieve(self, data):
        email = data["email"]
        password = data["password"]
        response = False
        if self.authenticate_user_credentials(email, password):
            response = True

        return json.dumps({'response': response})

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
            if (cursor != None):
                cursor.close()
            if (connection != None):
                self.db.disconnect(connection)
        return result

    def user_exists(self, email):
        """
        Check if a user exists in the database based on their email address
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
            cursor.execute(query, (email, ))
            count = cursor.fetchone()[0]
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if (cursor != None):
                cursor.close()
            if (connection != None):
                self.db.disconnect(connection)

        return count > 0

    def create_user(self, username, email, password):
        """
        Insert a new user into the database
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
                if (cursor != None):
                    cursor.close()
                if (connection != None):
                    self.db.disconnect(connection)

    def delete_user(self, email):
        """
        Delete a user from the database based on their email address
        """
        if self.user_exists(email):
            connection = None
            cursor = None
            try:
                connection = self.db.connect()
                cursor = connection.cursor()

                query = '''DELETE FROM Data WHERE userEmail = ?'''
                cursor.execute(query, (email))
            except sqlite3.Error as error:
                print("Error while connecting to sqlite", error)
            finally:
                if (cursor != None):
                    cursor.close()
                if (connection != None):
                    self.db.disconnect(connection)