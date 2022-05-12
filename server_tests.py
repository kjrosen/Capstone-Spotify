from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class FlaskTests_NoAccount(TestCase):

    def setUp(self):
        '''to do before each test'''
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()
        
        connect_to_db(app, 'testdb')
        db.create_all()
        example_data()

    def tearDown(self):
        '''to do after each test, ##TODO'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['login'] = False


    def test_homepage_route(self):
        '''test that the homepage is rendering'''
         
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h3 class="row">Most Popular Right Now</h3>', result.data)

    def test_login_route(self):
        '''gives login info for login, and confirms that the navbar updates with login info'''

        result = self.client.post('/login',
                                    data={
                                        'email': 'user1@gmail.com', 
                                        'password': 'one'},
                                    follow_redirects=True)
                                    
        self.assertIn(b'<a class="col" href="/mine">My Playlists</a>', result.data)

    def test_join_route(self):
        '''gives info for a new user, 
        tests that emails won't duplicate and new user created in test db
        tests that login information on route valid'''

        result_fail = self.client.post('/join', 
                                        data={
                                            'email':'user1@gmail.com', 
                                            'password':'1234',
                                            'name':'FailTester'},
                                        follow_redirects=True)
        
        result_success = self.client.post('/join', 
                                            data={
                                                'email':'SuccessTester@gmail.com',
                                                'password':'1234',
                                                'name':'SuccessTester'},
                                            follow_redirects=True)

        self.assertIn(b'<li>Email taken</li>', result_fail.data)
        self.assertIn(b'<a class="col" href="/mine">My Playlists</a>', result_success.data)


class FlaskTests_LoggedIn(TestCase):
    
    def setUp(self):
        '''to do before each test'''
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess['login'] = 1

        connect_to_db(app, 'testdb')
        db.create_all()
        example_data()

    def tearDown(self):
        '''to do after each test, ##TODO'''

        with self.client as c:
            with c.session_transaction() as sess:
                sess['login'] = False


    def test_logout_route(self):
        '''tests that a session data and html updates with logout'''

        result = self.client.get('/logout', follow_redirects=True)
        self.assertNotIn(b'<a class="col" href="/mine">My Playlists</a>', result.data)

    def test_verify_route(self):
        '''sets the session data to a set test user
        gives different password varieties to test the verify method'''

        result_success = self.client.post('/verify',
                                            data={
                                                'pw':'one'},
                                            follow_redirects=True)
        result_failure = self.client.post('/verify',
                                            data={
                                                'pw':'1234'},
                                            follow_redirects=True)

        self.assertIn(b'Type new name and/or password', result_success.data)
        self.assertNotIn(b'Wrong password', result_failure.data)



    # def test_myplays_route(self):
    #     '''tests that my-playlists is rendering'''

    #     result = self.client.get('/mine')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'<h3 class="row">Liked playlists</h3>', result.data)
        



if __name__ == "__main__":
    import unittest
    # If called like a script, run our tests
    unittest.main()