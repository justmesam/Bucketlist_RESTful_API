import json
from unittest import TestCase
from app import app, db_

class TestCaseItem(TestCase):
    """
    Testcases for the bucketlist items
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
    def bucketlist_id(self):
        """helps in getting the bucketlists id"""
        result = self.router('sammy1@gmail.com', '123456', 'register')
        token = json.loads(result.data.decode())['token_']
        response = self.app.post(
            '/bucketlists/',
            headers=dict(Authorization='Bearer ' + token),
            data=json.dumps({'title' : 'travel', 'intro' : 'go to the moon'}),
            content_type='application/json'
        )
        _id = json.loads(response.data.decode())['id']
        return dict(_id=_id, token=token)

    def test_item_creation(self):
        """
        Tests for creating an item
        """
        data = self.bucketlist_id()
        response = self.app.post(
            '/bucketlists/{}/items/'.format(data['_id']),
            headers=dict(Authorization='Bearer ' + data['token']),
            data=json.dumps({'title' : 'Adventure', 'intro' : 'sky diving'}),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data["intro"] == "sky diving")
        self.assertTrue(data["id"])

    def test_list_all_bucketlists_items(self):
        """
        Tests for listing all bucketlist items and pagination
        """
        data_ = self.bucketlist_id()
        response = self.app.post(
            '/bucketlists/{}/items/'.format(data_['_id']),
            headers=dict(Authorization='Bearer ' + data_['token']),
            data=json.dumps({'title' : 'Adventure', 'intro' : 'sky diving'}),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(response.status_code, 201)

        response = self.app.get(
            '/bucketlists/{}/items/'.format(data_['_id']),
            headers=dict(Authorization='Bearer ' + data_['token']),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, list)
        self.assertIn('Adventure', str(response.data))

        # test for pagination
        response = self.app.get(
            '/bucketlists/{}/items/?limit=2&page=1'.format(data_['_id']),
            headers=dict(Authorization='Bearer ' + data_['token']),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, dict)
        self.assertIn('next_page', str(response.data))
        self.assertIn('sky diving', str(response.data))
        self.assertIn('previous_page', str(response.data))

    def test_get_update_and_delete(self):
        """
        Tests for get, update and delete of a bucketlist item using its id
        """
        data_ = self.bucketlist_id()
        response = self.app.post(
            '/bucketlists/{}/items/'.format(data_['_id']),
            headers=dict(Authorization='Bearer ' + data_['token']),
            data=json.dumps({'title' : 'Adventure', 'intro' : 'sky diving'}),
            content_type='application/json'
        )
        self.assertTrue(response.status_code, 201)
        item_id = json.loads(response.data.decode())['id']

        response_update = self.app.put(
            '/bucketlists/{}/items/{}/'.format(data_['_id'], item_id),
            headers=dict(Authorization='Bearer ' + data_['token']),
            data=json.dumps({'title' : 'Adventure and risks', 'intro' : 'sky diving and bungee jumping'}),
            content_type='application/json'
        )
        response_data = json.loads(response_update.data.decode())
        self.assertTrue(response_data['title'] == 'Adventure and risks')
        self.assertTrue(response_data['id'])
        self.assertTrue(response_update.status_code, 200)

        response = self.app.get(
            '/bucketlists/{}/items/{}/'.format(data_['_id'], item_id),
            headers=dict(Authorization='Bearer ' + data_['token']),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, dict)
        self.assertIn('sky diving and bungee jumping', str(response.data))

        response = self.app.delete(
            '/bucketlists/{}/items/{}/'.format(data_['_id'], item_id),
            headers=dict(Authorization='Bearer ' + data_['token']),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, dict)
        self.assertIn('item deleted', str(response.data))


if __name__ == '__main__':
    unittest.main()
