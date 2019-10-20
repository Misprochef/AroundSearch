from flask import (
    Flask,
    render_template,
    request,
    logging,
    Response,
    redirect,
    flash,
    url_for,
    session,
)
from datetime import datetime
from myapp import app
from myapp.models import User, Page
from flask_login import current_user, login_required


def UserInfo():
    try:
        pages = Page.query.filter_by(user_id=current_user.id).all()
        return pages
    except:
        pass


# userinfo = UserInfo() これを挟むとpagesが表示されない なぜだろう


@app.route("/")
def input():
    if not UserInfo():
        return render_template("input.html")
    else:
        return render_template("input.html", pages=UserInfo())


@app.route("/output", methods=["POST"])
def output():
    keyword = request.form["keyword"]
    keyword_on_site = str(request.form["keyword"] + " site:")
    if not UserInfo():
        return render_template(
            "output.html", keyword=keyword, keyword_on_site=keyword_on_site
        )
    else:
        return render_template(
            "output.html",
            keyword=keyword,
            keyword_on_site=keyword_on_site,
            pages=UserInfo(),
        )
