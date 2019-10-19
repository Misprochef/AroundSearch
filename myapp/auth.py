from datetime import datetime

# import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# from werkzeug.security import check_password_hash, generate_password_hash
from myapp import db, login_manager, bcrypt
from myapp.forms import RegistrationForm, LoginForm
from myapp.models import User, Page
from flask_login import login_user, current_user, logout_user, login_required

bp_auth = Blueprint(
    "bp_auth", __name__, template_folder="templates", static_folder="static"
)


@bp_auth.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            "{} さん として登録しました 続けて登録したユーザー名・パスワードを入力しログインしてください".format(
                form.username.data
            ),
            "success",
        )
        return redirect(url_for("bp_auth.login"))
    return render_template("bp_auth/create_user.html", title="新規登録", form=form)


@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            # next_page = request.args.get("next")
            return redirect(url_for("input"))
        elif user is None:
            flash("ユーザー名が間違っています", "danger")
        else:
            flash("パスワードが間違っています", "danger")
    return render_template("bp_auth/login.html", title="ログイン", form=form)


@bp_auth.route("/logout")
def logout():
    logout_user()
    flash("ログアウトしました", "info")
    return redirect(url_for("input"))


# @bp_auth.before_app_request
# def load_logged_in_user():
#     """
#     どのURLが要求されても、ビュー関数の前で実行される関数
#     ログインしているか確認し、ログインされていればユーザー情報を取得する
#     """
#     user_id = session.get("user_id")

#     if user_id is None:
#         g.user = None
#     else:
#         db = get_db()
#         g.user = db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


# def login_required(view):
#     """
#     ユーザーがログインされているかどうかをチェックし、
#     そうでなければログインページにリダイレクト
#     """

#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             flash("ログインをしてから操作してください", category="alert alert-warning")
#             return redirect(url_for("bp_auth.login"))

#         return view(**kwargs)

#     return wrapped_view
