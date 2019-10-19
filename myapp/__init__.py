"""
The flask application package.
"""
import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object("myapp.config")


db = SQLAlchemy(app)
db.init_app(app)

bcrypt = Bcrypt(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "bp_auth.login"
login_manager.login_message_category = "info"


import myapp.views

from myapp.auth import bp_auth

app.register_blueprint(bp_auth, url_prefix="/bp_auth")

from myapp.pages import bp_pages

app.register_blueprint(bp_pages, url_prefix="/bp_pages")

