import unittest
from datetime import datetime

class MockDatabase:
    def __init__(self):
        self.activities = []

    def enter_new_activity(self, client_name, client_email, client_password, activity_name, activity_date,
                           activity_starting_point, activity_duration):
        self.activities.append((client_name, client_email, client_password, activity_name, activity_date,
                                activity_starting_point, activity_duration))

    def free_time(self, email, meeting_date):
        """
        Retrieve the free time of a user on a specific date
        """
        # Get the user's activities for the specified date
        activities = [
            (start_time, duration) for _, activity_email, _, _, activity_date, start_time, duration in self.activities
            if activity_email == email and activity_date == meeting_date
        ]

        # Calculate the free time intervals between activities
        free_time_intervals = []
        prev_end_time = 0

        for activity in sorted(activities, key=lambda x: x[0]):
            start_time = activity[0]
            duration = activity[1]

            if start_time > prev_end_time:
                free_time_intervals.append((prev_end_time, start_time))

            prev_end_time = start_time + duration

        # Check if there is any free time after the last activity
        if prev_end_time < 24:  # Assuming 24-hour format
            free_time_intervals.append((prev_end_time, 24))

        return free_time_intervals


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db = MockDatabase()

    def tearDown(self):
        pass

    def test_free_time(self):
        # Insert sample activities for a user on a specific date
        user_email = 'user@example.com'
        activity_date = '2023-05-22'
        self.db.enter_new_activity('User', user_email, 'password', 'Activity 1', activity_date, 9, 2)
        self.db.enter_new_activity('User', user_email, 'password', 'Activity 2', activity_date, 14, 1)
        self.db.enter_new_activity('User', user_email, 'password', 'Activity 3', activity_date, 18, 3)

        # Calculate expected free time intervals
        expected_intervals = [(0, 9), (11, 14), (15, 18), (21, 24)]

        # Retrieve free time intervals from the mock database
        free_time_intervals = self.db.free_time(user_email, activity_date)

        # Compare the expected and retrieved intervals
        self.assertEqual(expected_intervals, free_time_intervals)


if __name__ == '__main__':
    unittest.main()
