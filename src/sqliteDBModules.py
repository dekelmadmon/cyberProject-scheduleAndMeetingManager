import sqlite3
import utils
class clientDatabase:
    def __init__(self, name, email, password): #initializes the database and enter basic data about user
        self.name=name
        self.email=email
        self.password=password

        try:
            sqliteConnection = sqlite3.connect('../db/SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE usersData (
                                            userName TEXT NOT NULL,
                                            userEmail text NOT NULL UNIQUE,
                                            userPassword text NOT NULL UNIQUE,
                                            userActivity text,
                                            startPoint REAL,
                                            duration REAL,);'''
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            sqlite_insert_basic_users_data='''INSERT INTO usersData (userName, userEmail, userPassword)
                                            VALUES (?, ?, ?)'''
            sqlite_insert_basic_users_data_args = (self.name,self.email,self.password)
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            cursor.execute(sqlite_insert_basic_users_data, sqlite_insert_basic_users_data_args)
            sqliteConnection.commit()
            print("SQLite table created")
            sqlite_select_Query = "select sqlite_version();"
            cursor.execute(sqlite_select_Query)
            record = cursor.fetchall()
            print("SQLite Database Version is: ", record)
            cursor.close()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if sqliteConnection:

                sqliteConnection.close()
                print("The SQLite connection is closed")
    def enterNewActivity(self,  activityX): #insert new row and store there name of activity starttime and endtime
        sqliteConnection = sqlite3.connect('usersInfodatabase.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        sqlite_insert_new_activity = '''INSERT INTO usersData (userName, userEmail, userPassword, userActivity, startPoint, duration)
                                            VALUES (?, ?, ?, ?, ?, ?)'''
        sqlite_insert_new_activity_args=(self.name,self.email,self.password,activityX.name, activityX.startingPoint, activityX.duration)
        cursor.execute(sqlite_insert_new_activity, sqlite_insert_new_activity_args)
        sqliteConnection.commit()
        cursor.close()

    def openCnnection(self):
        pass

