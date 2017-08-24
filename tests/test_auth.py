"""
All tests are here
"""
import json
from unittest import TestCase
from app import app, db_

class TestCaseAuth(TestCase):
    """
    Testcases for the auth eg login and register
    """
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        db_.session.close()
        db_.drop_all()
        db_.create_all()

        ###>>>> |||  Helper Method ||| <<<<###
    def router(self, email, password, route):
        """method helps in testing the register function"""
        return self.app.post('/auth/' + route + '/',
                             data=json.dumps(dict(email=email,
                                                  password=password)
                                            ),
                             content_type='application/json'
                            )

    def test_register_user(self):
        """
        Tests a user is registered successfully
        """
        result = self.router('samuel@email.com', '12345', 'register')
        data = json.loads(result.data.decode())
        self.assertTrue(result.status_code, 201)
        self.assertTrue(data['message'] == 'You have been successfuly registered')
        self.assertTrue(data['token_'])

    def test_for_a_registered_user(self):
        """
        Tests a user cannot be registered more than once
        """
        result = self.router('sam@email.com', '12345', 'register')
        data = json.loads(result.data.decode())
        self.assertTrue(data['message'] == 'You have been successfuly registered')
        self.assertTrue(result.status_code, 201)
        result2 = self.router('sam@email.com', '12345', 'register')
        data = json.loads(result2.data.decode())
        self.assertTrue(result2.status_code, 202)
        self.assertTrue(data['message'] == 'Email exists')

    def  test_login_for_registered_user(self):
        """
        Tests that a registered user can login
        """
        result = self.router('samuel1@email.com', '12345', 'register')
        self.assertTrue(result.status_code, 201)
        result_login = self.router('samuel1@email.com', '12345', 'login')
        data = json.loads(result_login.data.decode())
        self.assertTrue(result_login.status_code, 200)
        self.assertTrue(data['message'] == 'Successful Login')

    def test_login_unregistered_user(self):
        """
        Tests for an unregistered user
        """
        result_login = self.router('sammy@email.com', '12345', 'login')
        data = json.loads(result_login.data.decode())
        self.assertTrue(result_login.status_code, 401)
        self.assertTrue(data['message'] == 'You are not registered')

    def test_logout(self):
        """
        Tests for the user logout
        """
        result_register = self.router('sammy0@email.com', '12345', 'register')
        register_data = json.loads(result_register.data.decode())
        self.assertTrue(register_data['message'] == 'You have been successfuly registered')
        self.assertTrue(result_register.status_code, 201)

        response_register = self.app.post(
            '/auth/logout/',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    result_register.data.decode()
                )['token_'],
            ),
            content_type='application/json'
        )

        data_register = json.loads(response_register.data.decode())
        self.assertTrue(data_register['message'] == 'You have successfuly logged out')
        self.assertTrue(response_register.status_code, 200)


    def test_reset_password(self):
        """
        Tests when user resets password
        """
        result = self.router('samuel1@email.com', '0', 'reset_password')
        data = json.loads(result.data.decode())
        self.assertTrue(result.status_code, 200)
        self.assertTrue(data['message'] == 'Your password has been reset successfuly, you can change to a new password')
        self.assertTrue(data['new_password'])

    def test_change_password(self):
        """
        Tests for when the user changes their password
        """
        result_register = self.router('sammy1@email.com', '12345', 'register')
        self.assertTrue(result_register.status_code, 201)
        response = self.app.post(
            '/auth/change_password/',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    result_register.data.decode()
                )['token_']
            ),
            data=json.dumps(dict(old_password='12345',
                                 new_password='123456',
                                 confirm_password='123456')),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['message'] == 'You have changed the password successfuly')


    def test_delete_account(self):
        """
        Tests for when user delete account
        """
        result_register = self.router('sammy2@email.com', '12345', 'register')
        self.assertTrue(result_register.status_code, 201)
        response = self.app.post(
            '/auth/delete/',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    result_register.data.decode()
                )['token_']
            ),
            data=json.dumps(dict(password='12345')),
            content_type='application/json'
            )
        data = json.loads(response.data.decode())
        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['message'] == 'User successfuly deleted')


if __name__ == '__main__':
    unittest.main()
