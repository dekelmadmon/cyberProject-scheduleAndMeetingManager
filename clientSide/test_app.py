import unittest
import json
import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_page(self):
        response = self.app.get('/main')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login-page')
        self.assertEqual(response.status_code, 200)

    def test_sign_in_page(self):
        response = self.app.get('/sign-in-page')
        self.assertEqual(response.status_code, 200)

    def test_post_new_activity(self):
        data = json.dumps({"name": "test", "date": "2022-05-10", "start_time": "08:00:00", "end_time": "10:00:00"})
        response = self.app.post('/api/save-activity', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"name": "test", "date": "2022-05-10", "start_time": "08:00:00", "end_time": "10:00:00"})

    def test_sign_in_info(self):
        app.db = app.DBM.Database()
        app.db.delete_user('test@example.com')
        data = json.dumps({'username': 'test_user', 'email': 'test@example.com', 'password': 'test_password'})
        response = self.app.post('/api/sign-in', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        app.db.create_user('test_user', 'test@example.com', 'test_password')
        # Test case when user already exists
        response = self.app.post('/api/sign-in', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_info(self):
        app.db = app.DBM.Database()
        data = json.dumps({'username': 'test_user','email': 'test@example.com', 'password': 'test_password'})

        # Test case when user exists
        app.db.create_user('test_user', 'test@example.com', 'test_password')
        response = self.app.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'approved')

        app.db.delete_user('test@example.com')
        response = self.app.post('/api/login', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 401)



    def test_update_dates(self):
        # Test case when JSON data is invalid
        data = json.dumps({'invalid_key': 'invalid_value'})
        response = self.app.post('/update_schedule_dates', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test case when JSON data is missing key
        data = json.dumps({})
        response = self.app.post('/update_schedule_dates', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test case when JSON data is correct
        data = json.dumps({'factor': 3})
        response = self.app.post('/update_schedule_dates', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
