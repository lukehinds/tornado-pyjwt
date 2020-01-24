"""
    Tornado JSON Web Token example

    Generate a new token:
        http://localhost:8888/auth

    Request test:
        - Using the Postman and a "get method" request on <http://localhost:8888> with this header:
            Authorization:bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCIsImV4cCI6MTUwMjQ3Mjk5OX0.mTAC5izCCqE71jLWyGQtJRhbj12I79M7qBxbIrieSiE1

        replace token with your generated token

        curl --data "username=luke&password=password" http://localhost:8888/register
        curl --data "username=luke&password=password" http://localhost:8888/auth

    Requirements:
        PyJWT 1.5.2
        Tornado 4.51
        Python 3.6

        resources:
        https://gist.github.com/jslvtr/139cf76db7132b53f2b20c5b6a9fa7ad
        https://github.com/ivanzhirov/tornado-redis-angular-chat/

        need to decode to get role_id
        https://pyjwt.readthedocs.io/en/latest/usage.html#encoding-decoding-tokens-with-hs256

        Admin:
        admin password is 'admin' - the idea being users would change it immediately after deployment
"""

import tornado.ioloop
import tornado.web
import jwt
import datetime
from tornado.options import define, options
from auth import auth_handler
import os.path
import database
from werkzeug.security import generate_password_hash, check_password_hash

SECRET = 'my_secret_key'
PREFIX = 'Bearer '

class AuthHandler(tornado.web.RequestHandler):
    """
        Handle to auth method.
        This method aim to provide a new authorization token upon database credentials success
    """

    def get(self, *args, **kwargs):
        """
            return the generated token
        """
        
        username = self.get_argument("username")
        password = self.get_argument("password")
        if database.verify_user_credentials(username, password):
            details = database.get_account_details(username)
            group_id = details[3]
            role_id = details[4]

            self.encoded = jwt.encode({
                'group_id': group_id,
                'role_id': role_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)},
                SECRET,
                algorithm='HS256'
            )
            response = {'token': self.encoded.decode('ascii')}
            self.write(response)
        else:
            self.write('Auth Failed!')

@auth_handler
class MainHandler(tornado.web.RequestHandler):
    """
        Main page handler.
        Needs Authorization to access it with @jwfath decorator
    """

    def get(self, *args, **kwargs):
        # print(self.request.headers)
        token = self.request.headers.get("Authorization")[len(PREFIX):]
        decoded = jwt.decode(token, SECRET, algorithms='HS256')
        print(decoded)
        self.render('index.html')


@auth_handler
class UserHandler(tornado.web.RequestHandler):
    """
        Registration Handler
    """
    # get_account_details, if account is admin role, than allow them to register user
    def post(self):
        token = self.request.headers.get("Authorization")[len(PREFIX):]
        decoded = jwt.decode(token, SECRET, algorithms='HS256')
        if  decoded['role_id'] == '1':
            # add the user
            username = self.get_argument("username")  # maybe we can move these to __init__
            password = self.get_argument("password")
            group_id = self.get_argument("group_id")
            role_id = self.get_argument("role_id")
            database.create_account(username, password, group_id, role_id)
            self.write("%s user added successfully" % (username))
        else:
            self.write("role_id number %s is not authorised to register new users" % (decoded['role_id']))
        
    def delete(self):
        token = self.request.headers.get("Authorization")[len(PREFIX):]
        decoded = jwt.decode(token, SECRET, algorithms='HS256')
        username = self.get_argument("username") 
        if  decoded['role_id'] == '1':
            database.delete_account(username)
            self.write("%s user deleted successfully" % (username))

class TestRegisterHandler(tornado.web.RequestHandler):
    """
        Registration Handler with Auth (for testing only)
    """
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        group_id = self.get_argument("group_id")
        role_id = self.get_argument("role_id")
        database.create_account(username, password, group_id, role_id)

class Application(tornado.web.Application):
    """
        Application main class
    """

    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            'template_path': os.path.join(base_dir, "templates"),
            'static_path': os.path.join(base_dir, "static"),
            'debug': True,
            "xsrf_cookies": False,  # change me!
        }

        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/auth", AuthHandler, name="auth"),
            #tornado.web.url(r"/register", RegisterHandler, name="register"),
            tornado.web.url(r"/users", UserHandler, name="users"),
            tornado.web.url(r"/testregister", TestRegisterHandler, name="testregister"),
            tornado.web.url(r"/", MainHandler, name="main"),
        ], **settings)


if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
