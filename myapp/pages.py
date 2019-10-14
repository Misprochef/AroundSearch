"""
Webページ一覧の取得・新規追加・編集・削除を行う
"""

from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for, session

from werkzeug.exceptions import abort
from myapp.auth import login_required
from myapp.db import get_db

from myapp.instance.config import GOOGLE_KEYS
from googleapiclient.discovery import build

GOOGLE_API_KEY = GOOGLE_KEYS["GOOGLE_API_KEY"]
CUSTOM_SEARCH_ENGINE_ID = GOOGLE_KEYS["CUSTOM_SEARCH_ENGINE_ID"]

bp_pages = Blueprint(
    "bp_pages", __name__, template_folder="templates", static_folder="static"
)


@bp_pages.route("/")
@login_required
def index_pages():

    db = get_db()

    # Pageデータを取得
    user_id = session.get("user_id")
    pages = db.execute(
        "SELECT * FROM pages WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()

    # Page一覧画面へ遷移
    return render_template(
        "bp_pages/index_page.html", pages=pages, title="Pages", year=datetime.now().year
    )


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

    # 登録フォームから送られてきた値を取得

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

    if request.method == "POST":
        # Page登録処理

        # ユーザーIDを取得
        user_id = session.get("user_id")

        # DBと接続
        db = get_db()

        # エラーチェック
        error_message = None

        if not search_keyword:
            error_message = "Pageの入力は必須です"

        if error_message is not None:
            # エラーがあれば、それを画面に表示させる
            flash(error_message, category="alert alert-danger")
            return redirect(url_for("bp_pages.create_page"))

        # エラーがなければテーブルに登録する
        page_title = result_title
        page_url = result_link
        page_domain = result_display_link

        db.execute(
            "INSERT INTO pages (user_id, page_title, page_url, page_domain) VALUES (?, ?, ?, ?)",
            (user_id, page_title, page_url, page_domain),
        )
        # db.execute("INSERT INTO pages (order_number) VALUES (order_number + 1)")
        db.commit()

        # Page一覧画面へ遷移
        # flash("Pageが追加されました", category="alert alert-info")
        return redirect(url_for("bp_pages.index_pages"))


@bp_pages.route("/<int:page_id>/update_page", methods=("GET", "POST"))
@login_required
def update_page(page_id):
    """
    GET ：page更新画面に遷移
    POST：page更新処理を実施
    """
    pass


@bp_pages.route("/<int:page_id>/delete_page", methods=("GET", "POST"))
@login_required
def delete_page(page_id):
    """
    GET ：page削除確認画面に遷移
    POST：page削除処理を実施
    """
    # 書籍データの取得と存在チェック
    page = get_page_and_check(page_id)

    # if request.method == 'GET':
    #     # 書籍削除確認画面に遷移
    #     return render_template('book/delete_book.html',
    #                            book=book,
    #                            title='書籍の削除',
    #                            year=datetime.now().year)

    # 書籍の削除処理

    if page:
        db = get_db()
        db.execute("DELETE FROM pages WHERE id = ?", (page_id,))
        db.commit()

        # 書籍一覧画面へ遷移
        # flash('書籍が削除されました', category='alert alert-info')
        return redirect(url_for("bp_pages.index_pages"))


def get_page_and_check(page_id):
    """pageの取得と存在チェックのための関数"""
    # 書籍データの取得
    db = get_db()
    page = db.execute("SELECT * FROM pages WHERE id = ? ", (page_id,)).fetchone()

    if page is None:
        abort(404, "Sorry, page does not exist")

    return page
