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

    def disconnect(self):
        self.connection.close()

    def enter_new_activity(self, client_name, client_email, client_password, activity_name, activity_date,
                           activity_starting_point, activity_duration):
        """
        Insert a new row and store the name of activity, start time, and end time
        """
        self.connect()
        sqlite_insert_new_activity = ('''INSERT INTO Data (username, userEmail, userPassword, userActivity, activityDate, 
                                            startPoint, duration)
                                            VALUES (?, ?, ?, ?, ?, ?, ?)''')
        sqlite_insert_new_activity_args = (client_name, client_email, client_password, activity_name, activity_date,
                                           activity_starting_point, activity_duration)
        self.cursor.execute(sqlite_insert_new_activity, sqlite_insert_new_activity_args)
        self.connection.commit()
        self.disconnect()

    def sign_in(self, username, email, password):
        """
        Sign up a new user by inserting their details into the database
        """
        if not self.authenticate_user_credentials(email, password):
            self.create_user(username, email, password)
            return True
        return False

    def login_able(self, email, password):
        """
        Log in an existing user by checking their credentials against the database
        """
        return self.authenticate_user_credentials(email, password)

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

    def free_time(self, email, meeting_date):
        """
        Retrieve the free time of a user on a specific date
        """
        # Get the user's activities for the specified date
        query = '''
            SELECT startPoint, duration FROM Data
            WHERE userEmail = ? AND activityDate = ?
            ORDER BY startPoint
        '''
        self.cursor.execute(query, (email, meeting_date))
        activities = self.cursor.fetchall()

        # Calculate the free time intervals between activities
        free_time_intervals = []
        prev_end_time = 0

        for activity in activities:
            start_time = activity[0]
            duration = activity[1]

            if start_time > prev_end_time:
                free_time_intervals.append((prev_end_time, start_time))

            prev_end_time = start_time + duration

        # Check if there is any free time after the last activity
        if prev_end_time < 24:  # Assuming 24-hour format
            free_time_intervals.append((prev_end_time, 24))

        return free_time_intervals
