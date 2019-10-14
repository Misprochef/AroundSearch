"""
The flask application package.
"""
import os
from flask import Flask
from myapp.instance.config import CONFIG

SECRET_KEY = CONFIG["SECRET_KEY"]

app = Flask(__name__, instance_path=r"C:\Users\jiked\OneDrive\python\myapp\instance")
app.config.from_mapping(
    SECRET_KEY=SECRET_KEY, DATABASE=os.path.join(app.instance_path, "around_search.db")
)

from myapp.db import close_db

app.teardown_appcontext(close_db)

import myapp.views

from myapp.auth import bp_auth

app.register_blueprint(bp_auth, url_prefix="/bp_auth")

from myapp.pages import bp_pages

app.register_blueprint(bp_pages, url_prefix="/bp_pages")

# import myapp.get_search_responce


# if __name__ == "__main__":
# app.run(host="0.0.0.0", debug=False)
