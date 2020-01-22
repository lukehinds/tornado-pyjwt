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

"""
import tornado.ioloop
import tornado.web
import jwt
import datetime
from tornado.options import define, options
from auth import jwtauth
import os.path
from db import User
from werkzeug.security import generate_password_hash, check_password_hash

SECRET = 'my_secret_key'


@jwtauth  # decorator to enforce auth on Handler
class MainHandler(tornado.web.RequestHandler):
    """
        Main page handler.
        Needs Authorization to access it
        because here we're using @jwfath decorator
    """

    def get(self, *args, **kwargs):
        self.render('index.html')


# @jwtauth
class RegisterHandler(tornado.web.RequestHandler):
    """
        Registration Handler
    """

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        #group_id = self.get_argument("group_id")
        #role_id = self.get_argument("role_id")
        user = User.find_by_username(username)
        if user:
            self.write("Username %s is already registered" % (username))
        else:
            try:
                User(username, generate_password_hash(password)).save_to_db()
            except Exception as e:
                print('error: ',  e)
            self.write("username %s registered successfully" % (username))


class AuthHandler(tornado.web.RequestHandler):
    """
        Handle to auth method.
        This method aim to provide a new authorization token
        There is a fake payload (for tutorial purpose)
    """

    def prepare(self):
        """
            Encode a new token with JSON Web Token (PyJWT)
        """

        self.encoded = jwt.encode({
            'some': 'payload',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)},
            SECRET,
            algorithm='HS256'
        )

    def get(self, *args, **kwargs):
        """
            return the generated token
        """
        response = {'token': self.encoded.decode('ascii')}
        self.write(response)

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        group_id = self.get_argument("group_id")
        role_id = self.get_argument("role_id")

        user = User.find_by_username(username)
        if user and check_password_hash(user.password, password):
            print('User authenticated')
            response = {'token': self.encoded.decode('ascii')}
            self.write(response)
        else:
            self.write('Auth Failed!')


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
            tornado.web.url(r"/register", RegisterHandler, name="register"),
            tornado.web.url(r"/", MainHandler, name="main"),
        ], **settings)


if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
