import json
import random
import string
import time
import unittest

from itsdangerous import TimestampSigner
from passlib.hash import bcrypt_sha256

from app import db,app
from app.config import SECRET_KEY
from app.model import User, Client_View



class common_test_func(unittest.TestCase):

    def add_user(self):
        """Adds Test user to database"""
        try:
            user = User.query.filter_by(Client_id='testuser').first()
            db.session.delete(user)
            db.session.commit()
            user2 = User.query.filter_by(Client_id='testuser2').first()
            db.session.delete(user2)
            db.session.commit()
        except:
            pass
        pass_hash = bcrypt_sha256.encrypt("password", rounds=12)
        test_user_insert = User(Client_id='testuser',Password=pass_hash,api_key='api-key',current_login_ip='127.0.0.1')
        db.session.add(test_user_insert)
        db.session.commit()
        test_user_insert_2 = User(Client_id='testuser2',Password=pass_hash,api_key='api-key',current_login_ip='127.0.0.1')
        db.session.add(test_user_insert_2)
        db.session.commit()
        return test_user_insert

    def grab_api_key(self):
        """Grabs API Key for User"""
        self.add_user()
        temp_dic = {"Client_id":"testuser", "Password":"password"}
        post_return = self.app.post('/api_key',
                       data=json.dumps(temp_dic),
                       content_type='application/json')
        self.assertEqual(post_return.status_code, 200)
        content = json.loads(post_return.data)
        return content["API KEY"]

    def post_info(self):
        """Functions that Posts Data to the DB"""
        api_key = self.grab_api_key()
        temp_json = json.dumps({"case_name": "This is a case", "description": "About the Case",
                    "priority": 1, "product_area": "sales", "target_date": "10/21/2017"})
        post_return = self.app.post('api/client_view/testuser/' + api_key,
                       data=temp_json,
                       content_type='application/json')
        self.assertEqual(post_return.status_code, 200)
        output = []
        output.extend([api_key, temp_json])
        return output

    def login(self, username, password):
        return self.app.post('/', data='Client_id=' + username +'&Password=' + password,
                             follow_redirects=True,content_type='application/x-www-form-urlencoded')


    def logout(self):
        return self.app.get('/logout', follow_redirects=True)




class TestCase(common_test_func):

    def setUp(self):
        self.app = app
        self.app.config.from_object('app.config')
        self.app.config["NO_PASSWORD"] = False
        self.app.config["DEBUG"] = True
        self.app.config["TESTING"] = True
        self.app = app.test_client()
        db.create_all()



    def test_user_model(self):
        """Test added a User to temp.db and querying him with User model"""
        test_user_insert = self.add_user()
        test_user_query = User.query.all()
        assert test_user_insert in test_user_query

    def test_client_view_model(self):
        """Test added a User to temp.db and querying him with Client View model"""
        test_user_insert = Client_View(client_id = 'testuser',
                                         case_name= 'sample case',
                                         priority= '1',
                                         target_date = '10/7/2016',
                                         product_area = 'Engineering',
                                         status = 'In Progress',
                                         description= 'something'
                                         )
        db.session.add(test_user_insert)
        db.session.commit()
        test_user_query = Client_View.query.all()
        assert test_user_insert in test_user_query

    def test_general_api_security(self):
        ##TODO: Add General API security test
        """This Tests the API security that is checked before all POST and GET request"""
        get_return = self.app.get('/api/client_view/testuser/api_key')
        assert get_return.status_code == 400
        api_key = self.post_info()
        get_return = self.app.get('/api/client_view/fakeuser/' + api_key[0])
        assert get_return.status_code == 400
        user = User.query.filter_by(Client_id="testuser").first()
        user.current_login_ip = '127.0.0.2'
        db.session.commit()
        get_return = self.app.get('/api/client_view/testuser2/' + api_key[0])
        assert get_return.status_code == 400
        signer = TimestampSigner(SECRET_KEY)
        time.sleep(1)
        try:
            signer.unsign(api_key, max_age=1)
            raise
        except:
            pass




    def test_grab_api_key(self):
        """Test grabing API key and verify it's correct with
        what is stored in the Database"""
        api_key = self.grab_api_key()
        user = User.query.filter_by(Client_id="testuser").first()
        assert api_key in user.api_key

    def test_grab_api_key_error(self):
        """send fake credentials and fake API key"""
        fake_password = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(1000)])
        fake_user = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(1000)])
        temp_dic = {"Client_id":fake_user, "Password":fake_password}
        post_return = self.app.post('/api_key',
                       data=json.dumps(temp_dic),
                       content_type='application/json')
        self.assertEqual(post_return.status_code, 400)

        """Verify that only POST are allowed with API KEY"""
        get_return = self.app.get('/api_key')
        self.assertEqual(get_return.status_code, 405)


    def test_POST_api(self):
        """Test Posting data with API Key"""
        tempjson = self.post_info()
        tempjson = json.loads(tempjson[1])
        user = Client_View.query.filter_by(case_name="This is a case").first()
        assert user.case_name in tempjson[u'case_name']
        self.assertEqual(user.priority, tempjson[u'priority'])
        assert user.target_date in tempjson[u'target_date']
        assert user.product_area in tempjson[u'product_area']
        assert user.description in tempjson[u'description']

    def test_POST_api_error(self):
        """Test POST error handling"""
        ##TODO: Test POST error handling
        api_key = self.grab_api_key()
        temp_json = json.dumps({"case_name": "This is a case", "description": "About the Case",
                    "priority": "asdf", "product_area": "sales", "target_date": "asdfasdf"})
        post_return = self.app.post('api/client_view/testuser/' + api_key,
                       data=temp_json,
                       content_type='application/json')
        self.assertEqual(post_return.status_code, 400)




    def test_GET_api(self):
        """Test Grabing JSON data and comparing it to the Database"""
        api_key = self.post_info()
        user = Client_View.query.filter_by(case_name="This is a case").first()
        get_return = self.app.get('/api/client_view/testuser/' + api_key[0])
        content = json.loads(get_return.data)
        assert user.case_name in content[0][u'case_name']
        self.assertEqual(user.priority, content[0][u'priority'])
        assert user.target_date in content[0][u'target_date']
        assert user.product_area in content[0][u'product_area']
        assert user.status in content[0][u'status']
        assert user.description in content[0][u'description']


    def test_GET_api_error(self):
        """Test GET error handling, no test needed
        since user name is verified in API Security"""
        pass

    def test_login_logout(self):
        self.add_user()
        rv = self.login("   testuser  ", "   password   ")
        assert 'You have successfully logged in' in rv.data
        rv = self.logout()
        assert 'You have been logged out successfully' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Incorrect Credentials, please enter the correct Client Id and Password' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Incorrect Credentials, please enter the correct Client Id and Password' in rv.data
        rv = self.login('', 'defaultx')
        assert '[This field is required.]' in rv.data
        rv = self.login('', 'password')
        assert '[This field is required.]' in rv.data
        rv = self.login('testuser', '')
        assert '[This field is required.]' in rv.data



if __name__ == '__main__':
    unittest.main()





