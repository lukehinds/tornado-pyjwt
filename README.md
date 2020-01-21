# Tornado JWT Example

Simple Tornado App that hashes passwords to sqlite3 and then provides auth using
JWT.

Not robust or debugged a great deal, just something I put together to see how it
all works.

## Register user to DB

![Register](https://raw.githubusercontent.com/lukehinds/tornado-pyjwt/master/images/register.png)

## Authenticate User against DB and gain a JWT Token

![auth](https://raw.githubusercontent.com/lukehinds/tornado-pyjwt/master/images/auth.png)

## User JWT token to gain access to protected Handler

![post](https://raw.githubusercontent.com/lukehinds/tornado-pyjwt/master/images/post.png)