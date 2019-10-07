"""
DB接続と切断を行う
"""

import sqlite3
from flask import current_app, g

def get_db():
    """DBへの接続"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        # 列に名前でアクセスできるようにする
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """DBの切断"""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
