import json
from unittest import TestCase
from app import app, db_

class TestCaseBucketlist(TestCase):
    """
    Testcases for the bucketlist
    """
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            db_.session.close()
            db_.drop_all()
            db_.create_all()

    def router(self, email, password, route):
        """method helps in testing the routes functions"""
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
        token = json.loads(result.data.decode())['token_']

        response = self.app.post(
            '/bucketlists/',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps({'title' : 'travel', 'intro' : 'go to the moon'}),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data["id"])
        self.assertTrue(response.status_code, 201)

        response = self.app.get(
            '/bucketlists/',
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, list)
        self.assertIn('travel', str(response.data))

        # test for pagination
        response = self.app.get(
            '/bucketlists/?limit=2&page=1',
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, dict)
        self.assertIn('next_page', str(response.data))
        self.assertIn('travel', str(response.data))
        self.assertIn('previous_page', str(response.data))

    def test_get_update_and_delete(self):
        """
        Tests for get, update and delete of a bucketlist using its id
        """
        result = self.router('sammy@gmail.com', '123456', 'register')
        token = json.loads(result.data.decode())['token_']

        response = self.app.post(
            '/bucketlists/',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps({'title' : 'travel soon', 'intro' : 'go to the moon'}),
            content_type='application/json'
        )
        self.assertTrue(response.status_code, 201)
        _id = json.loads(response.data.decode())['id']

        response_update = self.app.put(
            '/bucketlists/{}/'.format(_id),
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps({'title' : 'travel soon alone', 'intro' : 'go to the moon and saturn'}),
            content_type='application/json'
        )
        response_data = json.loads(response_update.data.decode())
        self.assertTrue(response_data['title'] == 'travel soon alone')
        self.assertTrue(response_data['intro'] == 'go to the moon and saturn')
        self.assertTrue(response_data['id'])
        self.assertTrue(response_update.status_code, 201)

        response = self.app.get(
            '/bucketlists/{}/'.format(_id),
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, dict)
        self.assertIn('travel soon alone', str(response.data))

        response = self.app.delete(
            '/bucketlists/{}/'.format(_id),
            headers=dict(Authorization='Bearer ' + token),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, dict)
        self.assertIn('Bucketlist deleted', str(response.data))


if __name__ == '__main__':
    unittest.main()
