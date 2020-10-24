from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_gravatar import Gravatar
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)

gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False,\
	force_lower=False, use_ssl=False, base_url=None)

from app.routes import *