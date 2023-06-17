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

        # Insert a new row into the invitations table
        cursor.execute(
            """
            INSERT INTO invitations (clientemail, recipient, date, status)
            VALUES (?, ?, ?, ?)
            """,
            (data.get("email"), data.get("recipient"), data.get("date"), "pending"),
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

        # Insert a new row into the invitations table
        cursor.execute(
            """
            INSERT INTO invitations (clientemail, recipient, date, status)
            VALUES (?, ?, ?, ?)
            """,
            (data.get("email"), data.get("recipient"), data.get("date"), data.get("status")),
        )

        # Commit the changes
        connection.commit()

        # Close the database connection
        connection.close()