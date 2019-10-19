from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for, session

from werkzeug.exceptions import abort

# from myapp.auth import login_required
from myapp import db
from myapp.forms import PageForm
from myapp.models import User, Page
from flask_login import current_user, login_required

# from myapp.db import get_db

from myapp.config import GOOGLE_KEYS
from googleapiclient.discovery import build

GOOGLE_API_KEY = GOOGLE_KEYS["GOOGLE_API_KEY"]
CUSTOM_SEARCH_ENGINE_ID = GOOGLE_KEYS["CUSTOM_SEARCH_ENGINE_ID"]

bp_pages = Blueprint(
    "bp_pages", __name__, template_folder="templates", static_folder="static"
)


@bp_pages.route("/")
@login_required
def index_pages():
    pages = Page.query.all()
    return render_template("bp_pages/index_page.html", title="Pages", pages=pages)


@bp_pages.route("/create_page", methods=("GET", "POST"))
@login_required
def create_page():
    def getSearchResponse(keyword):
        # today = datetime.datetime.today().strftime("%Y%m%d")
        # timestamp = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")

        # makeDir(DATA_DIR)

        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

        page_limit = 1
        start_index = 1
        response = []
        for n_page in range(0, page_limit):
            try:
                # sleep(1)
                response.append(
                    service.cse()
                    .list(
                        q=keyword,
                        cx=CUSTOM_SEARCH_ENGINE_ID,
                        lr="lang_ja",
                        num=1,
                        start=start_index,
                    )
                    .execute()
                )
                start_index = (
                    response[n_page].get("queries").get("nextPage")[0].get("startIndex")
                )
            except Exception as e:
                print(e)
                break

        return response

    #     # 登録フォームから送られてきた値を取得

    if request.method == "POST":
        global search_keyword
        global result_title
        global result_display_link
        global result_link
        search_keyword = request.form["search_keyword"]
        result_title = getSearchResponse(search_keyword)[0]["items"][0]["title"]
        result_display_link = getSearchResponse(search_keyword)[0]["items"][0][
            "displayLink"
        ]
        result_link = getSearchResponse(search_keyword)[0]["items"][0]["link"]

        # page登録画面に遷移
        return render_template(
            "bp_pages/create_page.html",
            result_title=result_title,
            result_display_link=result_display_link,
            result_link=result_link,
            title="追加確認",
            year=datetime.now().year,
        )

    else:
        return render_template("bp_pages/create_page.html", title="Pageの追加")


@bp_pages.route("/index_page", methods=("GET", "POST"))
@login_required
def register_page():
    # form = PageForm()
    # if form.validate_on_submit():
    page = Page(
        user_id=current_user.id,
        page_title=result_title,
        page_url=result_link,
        page_domain=result_display_link,
    )
    db.session.add(page)
    db.session.commit()
    # flash()
    return redirect(url_for("bp_pages.index_pages"))


@bp_pages.route("/<int:page_id>/update_page", methods=("GET", "POST"))
@login_required
def update_page(page_id):
    pass


@bp_pages.route("/<int:page_id>/delete_page", methods=("GET", "POST"))
@login_required
def delete_page(page_id):
    page = Page.query.get(page_id)
    db.session.delete(page)
    db.session.commit()
    return redirect(url_for("bp_pages.index_pages"))


# def get_page_and_check(page_id):
#     """pageの取得と存在チェックのための関数"""
#     # 書籍データの取得
#     db = get_db()
#     page = db.execute("SELECT * FROM pages WHERE id = ? ", (page_id,)).fetchone()

#     if page is None:
#         abort(404, "Sorry, page does not exist")

#     return page
