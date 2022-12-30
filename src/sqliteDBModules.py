import sqlite3
from . import main
import sqlite3
import time
import os
import datetime
from os.path import abspath

class Database(object):
    def __init__(self):
        """Initialize db class variables"""
        self.directory = abspath(r'..\db\SQLite_Python.db')
        self.connection = sqlite3.connect(self.directory)
        self.cur = self.connection.cursor()

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

            sqlite_select_Query = "select sqlite_version();"
            cursor.execute(sqlite_select_Query)
            record = cursor.fetchall()
            print("SQLite Database Version is: ", record)
            cursor.close()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if sqlite_connection:

                sqlite_connection.close()
                print("The SQLite connection is closed")

    def enterNewActivity(self,  activityX, client): #insert new row and store there name of activity starttime and endtime
        print("Successfully Connected to SQLite")
        sqlite_insert_new_activity = ('''INSERT INTO usersData (userName, userEmail, userPassword, userActivity, startPoint, duration)
                                            VALUES (?, ?, ?, ?, ?, ?)''')
        sqlite_insert_new_activity_args=(client.name, client.email, client.password, activityX.name, activityX.startingPoint, activityX.duration)
        self.cursor.execute(sqlite_insert_new_activity, sqlite_insert_new_activity_args)
        self.commit()
    def getDB(self):
            for row in self.usersData:
                pass

    def openCnnection(self):
        pass

