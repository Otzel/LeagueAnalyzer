import streamlit.web.cli as stcli
import sys
import os
from core.database import initialize_database

APP_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "app/app.py"))


if __name__ == "__main__":
    initialize_database()
    sys.argv = ["streamlit", "run", APP_FILE]
    stcli.main()


