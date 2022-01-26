"""
Modul zawierajacy zmienne ustawien dla aplikacji flask
"""

import os
from datetime import timedelta

# -- Server Config -- #
PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_FOLDER = os.path.join(PATH, "source", "WarstwaPrezentacji", "templates")
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True
PERMANENT_SESSION_LIFETIME = timedelta(days=1)
SECRET_KEY = ""

# -- Database Config -- #
TEST_DATABASE_URI = "sqlite:///:memory:"
PRODUCTION_DATABASE_URI = "sqlite:///{}".format(os.path.join(PATH, ""))
CHECK_SAME_THREAD_DB = False

# -- Mail Config -- #

SYS_MAIL = ''
SYS_MAIL_PSW = ''

DO_UNIT_TESTS_BEFORE = False
