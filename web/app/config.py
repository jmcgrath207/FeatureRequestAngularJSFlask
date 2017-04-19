from jinja2 import Undefined
import os

# Without this get_auth_token via POST request w/ JSON data does not work
# You keep getting "CSRF token missing" error
WTF_CSRF_ENABLED = False
#SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
SECRET_KEY = "FLASK_SECRET_KEY"

#Correct the issue where Jinja2 will error out if variable is not defined
JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined }


#NO_PASSWORD = False
NO_PASSWORD = True
DEBUG = False


response = os.system("ping -c 5 mysql")


if response != 0:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
else:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s" % (
        "root",
        os.environ["MYSQL_ROOT_PASSWORD"],
        os.environ["MYSQL_HOSTNAME"],
        os.environ["MYSQL_PORT"],
        os.environ["MYSQL_DATABASE"])


SQLALCHEMY_BINDS = {
    'auth_user': SQLALCHEMY_DATABASE_URI,
    'auth_role' : SQLALCHEMY_DATABASE_URI,
    'Client_View': SQLALCHEMY_DATABASE_URI,
}

#Flask-Security Config
SECURITY_TRACKABLE = True