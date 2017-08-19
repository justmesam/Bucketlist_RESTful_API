"""
All tests are here
"""
import json
from unittest import TestCase
from app import app

class TestCaseAuth(TestCase):
    """
    Testcases for the auth eg login and register
    """
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        ###>>>> |||  Helper Method ||| <<<<###
    def register(self, email, password):
        """method helps in testing the register function"""
        return self.app.post('/auth/register',
                             data=json.dumps(dict(email=email,
                                                  password=password)
                                            )
                            )
    def login(self, email, password):
        """method helps in testing login function"""
        return self.app.post('/auth/login',
                             data=json.dumps(dict(email=email,
                                                  password=password)
                                            )
                            )
    def test_register_user(self):
        """
        Tests a user is registered successfully
        """
        result = self.register('sam@email.com', '12345')
        data = json.loads(result.data.decode())
        self.assertTrue(result.status_code, 201)
        self.assertTrue(data['message'] == 'You have been successfuly registered')
        self.assertTrue(data['token_'])

    def test_for_a_registered_user(self):
        """
        Tests a user cannot be registered more than once
        """
        result = self.register('sam@email.com', '12345')
        data = json.loads(result.data.decode())
        self.assertTrue(data['message'] == 'You have been successfuly registered')
        self.assertTrue(result.status_code, 201)
        result2 = self.register('sam@email.com', '12345')
        data = json.loads(result.data.decode())
        self.assertTrue(result2.status_code, 202)
        self.assertTrue(data['message'] == 'Email exists')

    def  test_login_for_registered_user(self):
        """
        Tests that a registered user can login
        """
        result = self.register('sam@email.com', '12345')
        self.assertTrue(result.status_code, 201)
        result_login = self.login('sam@email.com', '12345')
        data = json.loads(result.data.decode())
        self.assertTrue(result_login.status_code, 200)
        self.assertTrue(data['message'] == 'Successful Login')

    def test_for_login_unregistered_user(self):
        """
        Tests for an unregistered user
        """
        result_login = self.login('sam@email.com', '12345')
        data = json.loads(result_login.data.decode())
        self.assertTrue(result_login.status_code, 401)
        self.assertTrue(data['message'] == 'You are not registered')

if __name__ == '__main__':
    unittest.main()
