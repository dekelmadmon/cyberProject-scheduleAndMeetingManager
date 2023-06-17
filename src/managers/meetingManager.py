import sqlite3
import json

from src.managers.managerInterface import ManagerInterface
from src.model.meeting import Meeting
from src.utils.MeetingEncoder import MeetingEncoder


class MeetingManager(ManagerInterface):
    def __init__(self, db_path):
        self.db_path = db_path
        print("Init")

    def create(self, data):
        # Connect to the temporary SQLite database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Check if the row already exists
        cursor.execute(
            """
            SELECT COUNT(*) FROM invitations
            WHERE clientemail = ? AND recipient = ? AND date = ?
            """,
            (data.get("email"), data.get("recipient"), data.get("date")),
        )
        row_count = cursor.fetchone()[0]

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

        # Close the database connection
        connection.close()

    def retrieve(self, data):
        # Connect to the temporary SQLite database
        connection = sqlite3.connect(self.db_path)
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
        invitations = []
        invitation = cursor.fetchone()
        while invitation != None:
            meeting = Meeting(invitation[0],invitation[1],invitation[2],invitation[3])
            invitations.append(meeting)
            invitation = cursor.fetchone()
        cursor.fetchone()
        print("Invitations:", json.dumps(invitations, cls=MeetingEncoder))

        # Close the database connection
        connection.close()

        return json.dumps(invitations, cls=MeetingEncoder)

    def update(self, data):
        # Connect to the temporary SQLite database
        connection = sqlite3.connect(self.db_path)
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

        #print("Updated", cursor.rowcount, query, data)

        # Commit the changes
        connection.commit()

        # Close the database connection
        connection.close()