import streamlit.web.cli as stcli
import sys
import os
from core.database import initialize_database, insert_match, fetch_all_matches
from core.dataHandler import update_database

APP_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "app/app.py"))


if __name__ == "__main__":
    sys.argv = ["streamlit", "run", APP_FILE]
    stcli.main()


