import sqlite3
from os.path import abspath

class Database(object):
    def __init__(self):
        """Initialize db class variables"""
        self.directory = abspath(r'..\db\SQLite_Python.db')
        self.connection = sqlite3.connect(self.directory)
        self.cur = self.connection.cursor()
        sqlite_connection = False
        try:
            sqlite_connection = sqlite3.connect('../db/SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS Data (
                                            id INTEGER PRIMARY KEY,
                                            userName TEXT NOT NULL,
                                            userEmail TEXT NOT NULL UNIQUE,
                                            userPassword TEXT NOT NULL,
                                            userActivity TEXT,
                                            activityDate TEXT,
                                            startPoint REAL,
                                            duration REAL);'''
            cursor = sqlite_connection.cursor()
            cursor.execute(sqlite_create_table_query)
            sqlite_select_query = "SELECT sqlite_version();"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            print("SQLite Database Version is: ", record)
            cursor.close()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("The SQLite connection is closed")

    # Insert a new row and store the name of activity, start time, and end time
    def enter_new_activity(self, client_name, client_email, client_password, activity_name, activity_date,
                           activity_starting_point, activity_duration):
        print("Successfully Connected to SQLite")
        sqlite_insert_new_activity = ('''INSERT INTO Data (userName, userEmail, userPassword, userActivity, activityDate, 
                                            startPoint, duration)
                                            VALUES (?, ?, ?, ?, ?, ?, ?)''')
        sqlite_insert_new_activity_args = (client_name, client_email, client_password, activity_name, activity_date,
                                           activity_starting_point, activity_duration)
        self.cur.execute(sqlite_insert_new_activity, sqlite_insert_new_activity_args)
        self.connection.commit()

    # Authenticate user login credentials
    def login(self, email, password):
        sqlite_search = '''SELECT userEmail FROM Data WHERE userEmail=? AND userPassword=?'''
        self.cur.execute(sqlite_search, (email, password))
        result = self.cur.fetchall()
        if result:
            return True
        else:
            return False

    # Check if user with given email and password exists in the database
    def user_exist(self, email, password):
        sqlite_search = '''SELECT userEmail FROM Data WHERE userEmail=?'''
        self.cur.execute(sqlite_search, (email,))
        result = self.cur.fetchall()
        if result:
            sqlite_search = '''SELECT userEmail FROM Data WHERE userEmail=? AND userPassword=?'''
            self.cur.execute(sqlite_search, (email, password))
            result = self.cur.fetchall()
            if result:
                return True
            else:
                return False
        else:
            return False

    # Open database connection
    def open_connection(self):
        pass
