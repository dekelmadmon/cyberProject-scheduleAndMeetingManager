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
        self.directory =abspath(r'..\db\SQLite_Python.db')
        self.connection = sqlite3.connect(self.directory)
        self.cur = self.connection.cursor()

    def deleteAllData(self):
        self.cur.execute("DELETE FROM data;")

    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    def execute(self, new_data):
        """execute a row of data to current cursor"""
        self.cur.execute(new_data)

    def executemany(self, many_new_data):
        """add many new data to database in one go"""
        self.cur.executemany('INSERT INTO data (unix, datestamp, item, publishername, value) VALUES(?, ?, ?, ?, ?)', many_new_data)
        self.commit()

    def create_table(self):
        """create a database table if it does not exist already"""
        self.cur.execute('''CREATE TABLE data(unix REAL,
                                            datestamp TEXT,
                                            item TEXT ,
                                            publishername TEXT,
                                            value INTEGER)''')
    def commit(self):
        """commit changes to database"""
        self.connection.commit()

    def databaseSetup(self):
        self.create_table()
        self.commit()

    def insertNewData(self, Item, publisherName, Price):
        unix = int(time.time())
        date = datetime.datetime.now()


class ClientDatabase:
    def __init__(self):
        """Initialize db class variables"""
        self.directory = abspath(r'..\db\SQLite_Python.db')
        self.connection = sqlite3.connect(self.directory)
        self.cur = self.connection.cursor()

        try:
            sqlite_connection = sqlite3.connect('../db/SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE usersData (
                                            userName TEXT NOT NULL,
                                            userEmail text NOT NULL UNIQUE,
                                            userPassword text NOT NULL UNIQUE,
                                            userActivity text,
                                            startPoint REAL,
                                            duration REAL,);'''
            cursor = sqlite_connection.cursor()
            print("Successfully Connected to SQLite")
            sqlite_insert_basic_users_data='''INSERT INTO usersData (userName, userEmail, userPassword)
                                            VALUES (?, ?, ?)'''
            sqlite_insert_basic_users_data_args = (self.name,self.email,self.password)
            cursor.execute(sqlite_create_table_query)
            sqlite_connection.commit()
            cursor.execute(sqlite_insert_basic_users_data, sqlite_insert_basic_users_data_args)
            sqlite_connection.commit()
            print("SQLite table created")
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
    def create_database_users_table(self):
        sqlite_create_table_query = '''CREATE TABLE usersData (
                                        userID text NOT NULL PRIMARY.
                                        userName TEXT NOT NULL,
                                        userEmail text NOT NULL,
                                        userPassword text NOT NULL UNIQUE,);'''
    def create_database_activity_table(self):
        sqlite_create_table_query = '''CREATE TABLE activityData(
                                                    userID text NOT NULL PRIMARY,
                                                    userActivity text,
                                                    startPoint REAL,
                                                    duration REAL,)'''
    def enterNewActivity(self,  activityX): #insert new row and store there name of activity starttime and endtime
        print("Successfully Connected to SQLite")
        sqlite_insert_new_activity = ('''INSERT INTO usersData (userName, userEmail, userPassword, userActivity, startPoint, duration)
                                            VALUES (?, ?, ?, ?, ?, ?)''')
        sqlite_insert_new_activity_args=(self.name, self.email, self.password, activityX.name, activityX.startingPoint, activityX.duration)
        self.cursor.execute(sqlite_insert_new_activity, sqlite_insert_new_activity_args)
        self.commit()
    def getDB(self):
            for row in self.usersData:
                pass

    def openCnnection(self):
        pass

