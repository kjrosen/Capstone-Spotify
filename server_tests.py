from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class FlaskTests(TestCase):

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

    def test_homepage_route(self):
        '''test that the homepage is rendering'''
         
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h3 class="row">Most Popular Right Now</h3>', result.data)

    def test_login_route(self):
        '''gives login info for login, and confirms that the navbar updates with login info'''

        result = self.client.post('/login',
                                    data={
                                        'email': 'hbplaymaker@gmail.com', 
                                        'password': 'bossbaby'},
                                    follow_redirects=True)
                                    
        self.assertIn(b'<a class="col" href="/mine">My Playlists</a>', result.data)

    def test_join_route(self):
        '''gives info for a new user, 
        tests that emails won't duplicate and new user created in test db
        tests that login information on route valid'''

        result_fail = self.client.post('/join', 
                                        data={
                                            'email':'hbplaymaker@gmail.com', 
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


    def test_logout_route(self):
        '''tests that a session data and html updates with logout'''

        



    # def test_myplays_route(self):
    #     '''tests that my-playlists is rendering'''

    #     result = self.client.get('/mine')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'<h3 class="row">Liked playlists</h3>', result.data)
        



if __name__ == "__main__":
    import unittest
    # If called like a script, run our tests
    unittest.main()