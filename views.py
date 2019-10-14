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
from myapp.db import get_db

# app = Flask(__name__)


def UserInfo():
    try:
        db = get_db()

        user_id = session.get("user_id")
        # global pages
        pages = db.execute(
            "SELECT * FROM pages WHERE user_id = ? ORDER BY id DESC", (user_id,)
        ).fetchall()

        return pages
    except:
        pass


# userinfo = UserInfo() これを挟むとpagesが表示されない なぜだろう


@app.route("/")
def input():
    if not UserInfo():
        return render_template("input.html", year=datetime.now().year)
    else:
        return render_template("input.html", pages=UserInfo(), year=datetime.now().year)


# @app.route("/output", methods = ["POST"])
# def output():
#         keyword = request.form["keyword"]
#         return redirect(url_for("redirect_test",
#                keyword = keyword))

# @app.route("/redirect_test", methods=["GET"])
# def redirect_test():
#     keyword = request.args.get("keyword", "")
#     return render_template("output.html", keyword = keyword)


@app.route("/output", methods=["POST"])
def output():
    keyword = request.form["keyword"]
    keyword_on_site = str(request.form["keyword"] + " site:")
    if not UserInfo():
        return render_template(
            "output.html",
            keyword=keyword,
            keyword_on_site=keyword_on_site,
            year=datetime.now().year,
        )
    else:
        return render_template(
            "output.html",
            keyword=keyword,
            keyword_on_site=keyword_on_site,
            pages=UserInfo(),
            year=datetime.now().year,
        )


# @login_required
# @app.route("/")
# def input():
#     db = get_db()

#     user_id = session.get("user_id")
#     global pages
#     pages = db.execute(
#         "SELECT * FROM pages WHERE user_id = ? ORDER BY id DESC", (user_id,)
#     ).fetchall()

#     return render_template("input.html", pages=pages, year=datetime.now().year)


# @login_required
# @app.route("/output", methods=["POST"])
# def output():
#     keyword = str(request.form["keyword"] + " site:qiita.com")
#     return render_template(
#         "output.html", keyword=keyword, pages=pages, year=datetime.now().year
#     )


# if __name__ == "__main__" :
# app.run(host="0.0.0.0", debug=False) __init__でなく、ここにこの記述を入れるとhtmlのurl_forがうまく動かない なぜだろう
