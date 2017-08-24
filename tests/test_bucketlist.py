import json
from unittest import TestCase
from app import app

class TestCaseBucketlist(TestCase):
    """
    Testcases for the bucketlist
    """
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def router(self, email, password, route):
        """method helps in testing the register function"""
        return self.app.post('/auth/' + route + '/',
                             data=json.dumps(dict(email=email,
                                                  password=password)
                                            ),
                             content_type='application/json'
                            )
    def test_bucketlist_creation(self):
        """
        Tests for creating the bucketlist
        """
        result = self.router('sammy1@gmail.com', '123456', 'register')
        print(result.data)
        token = json.loads(result.data.decode())['token_']

        response = self.app.post(
            '/bucketlists/',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps({'title' : 'travel', 'intro' : 'go to the moon'}),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data["intro"] == "go to the moon")
        self.assertTrue(data["id"])

    def test_list_all_bucketlists(self):
        """
        Tests for listing all users bucketlist
        """
        result = self.router('sammy@gmail.com', '123456', 'register')
        print(result.data)
        token = json.loads(result.data.decode())['token_']

        response = self.app.post(
            '/bucketlists/',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps({'title' : 'travel', 'intro' : 'go to the moon'}),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        print(data)
        self.assertTrue(data["id"])

        response = self.app.get(
            '/bucketlists/',
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, list)
        self.assertIn('travel', str(response.data))
