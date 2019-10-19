import os

CONFIG = {"SECRET_KEY": "b'@\xa9\xfd:\x83\x95\xe4mG\x12r\x80]Z-\xa7'"}

GOOGLE_KEYS = {
    "GOOGLE_API_KEY": "AIzaSyCn1T_tw2elMmdr57OJQmv3qp_c-qFYC1w",
    "CUSTOM_SEARCH_ENGINE_ID": "018135131531454067016:qp0rc0xr4tz",
}

SECRET_KEY = b'*\x06\xa5\xab=\xa6\x88%E\xcd"\xb7\xba\x10\xc9S'

SQLALCHEMY_DATABASE_URI = (
    os.environ.get("DATABASE_URL") or "sqlite:///around_search_pg.db"
)
SQLALCHEMY_TRACK_MODIFICATIONS = True
