import sqlite3
import json
from src import sqliteDBModule
from src.managers.managerInterface import ManagerInterface
from src.model.meeting import Meeting
from src.utils.MeetingEncoder import MeetingEncoder


class MeetingManager(ManagerInterface):
    def __init__(self):
        self.db = sqliteDBModule.Database()
        print("Init")

    def create(self, data):
        # Connect to the temporary SQLite database
        connection = None
        cursor = None
        try:
            connection = self.db.connect()
            cursor = connection.cursor()

            # Check if the row already exists
            cursor.execute(
                """
                SELECT COUNT(*) FROM invitations
                WHERE clientemail = ? AND recipient = ? AND date = ?
                """,
                (data.get("email"), data.get("recipient"), data.get("date")),
            )
            result = cursor.fetchone()[0]

            row_count = result

            if row_count == 0:
                # Insert a new row if it doesn't exist
                cursor.execute(
                    """
                    INSERT INTO invitations (clientemail, recipient, date, status)
                    VALUES (?, ?, ?, ?)
                    """,
                    (data.get("email"), data.get("recipient"), data.get("date"), "pending"),
                )
            else:
                # Update the existing row
                cursor.execute(
                    """
                    UPDATE invitations SET status = ?
                    WHERE clientemail = ? AND recipient = ? AND date = ?
                    """,
                    ("pending", data.get("email"), data.get("recipient"), data.get("date")),
                )

            # Commit the changes
            connection.commit()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if (cursor != None):
                cursor.close()
            if (connection != None):
                self.db.disconnect(connection)

    def retrieve(self, data):
        # Connect to the temporary SQLite database
        connection = None
        cursor = None
        invitations = []

        try:
            connection = self.db.connect()
            cursor = connection.cursor()

            # Retrieve pending invitations for the participant's email
            cursor.execute(
                    """
                SELECT *
                FROM invitations
                WHERE  ?  IN (recipient, clientemail)
                """,
                (data.get("email"),),
            )

            invitation = cursor.fetchone()
            while invitation != None:
                meeting = Meeting(invitation[0], invitation[1], invitation[2], invitation[3])
                invitations.append(meeting)
                invitation = cursor.fetchone()
            cursor.fetchone()
            print("Invitations:", json.dumps(invitations, cls=MeetingEncoder))

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if (cursor != None):
                cursor.close()
            if (connection != None):
                self.db.disconnect(connection)

        return json.dumps(invitations, cls=MeetingEncoder)

    def update(self, data):

        # Connect to the temporary SQLite database
        connection = None
        cursor = None
        invitations = []

        try:
            connection = self.db.connect()
            cursor = connection.cursor()

            query = """
                UPDATE invitations SET status = ?
                WHERE clientemail = ? AND recipient = ? AND date = ? and status <> "Canceled"
                """
            # Insert a new row into the invitations table
            cursor.execute(
                query,
                (data.get("status"), data.get("requester"), data.get("recipient"), data.get("date")),
            )

            # Commit the changes
            connection.commit()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if (cursor != None):
                cursor.close()
            if (connection != None):
                self.db.disconnect(connection)