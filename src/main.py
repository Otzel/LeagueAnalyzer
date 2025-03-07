import streamlit.web.cli as stcli
import sys
import os

APP_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "app/app.py"))

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", APP_FILE]
    stcli.main()