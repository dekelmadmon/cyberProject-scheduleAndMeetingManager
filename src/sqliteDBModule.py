import sqlite3
from . import useless
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
            sqlite_create_table_query = '''CREATE TABLE Data (
                                            userName TEXT NOT NULL,
                                            userEmail text NOT NULL UNIQUE,
                                            userPassword text NOT NULL UNIQUE,
                                            userActivity text,
                                            startPoint REAL,
                                            duration REAL,);'''
            cursor = sqlite_connection.cursor()

            sqlite_select_query = "select sqlite_version();"
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

    def enter_new_activity(self,  client_name, client_email, client_password, activityX_name, activityX_startingPoint, activityX_duration): #insert new row and store there name of activity starttime and endtime
        print("Successfully Connected to SQLite")
        sqlite_insert_new_activity = ('''INSERT INTO Data (Name, Email, Password, Activity, startPoint, duration)
                                            VALUES (?, ?, ?, ?, ?, ?)''')
        sqlite_insert_new_activity_args=(client_name, client_email, client_password, activityX_name, activityX_startingPoint, activityX_duration)
        self.cur.execute(sqlite_insert_new_activity, sqlite_insert_new_activity_args)
        self.connection.commit()
    def user_exist(self, email):
        sqlite_search = ('''SELECT Email FROM data WHERE Email = ?''')
        self.cur.execute(sqlite_search, email)
        print (self.cur.fetchall())
        if (self.cur.fetchall()):
            return True
        return False


    def open_connection(self):
        pass


