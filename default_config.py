import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
DEBUG = False
SECRET_KEY = 'your_secret_key'
WTF_CSRF_ENABLED = True
PUSHOVER_API_KEY = "your_pushover_api_key"
PUSHOVER_USER_KEY = "your_pushover_user_key"
