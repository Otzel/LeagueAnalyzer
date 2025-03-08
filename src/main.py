import streamlit.web.cli as stcli
import sys
import os
from core.database import initialize_database, insert_match, fetch_all_matches
from core.dataHandler import update_database

APP_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "app/app.py"))
test_data = {}
test_data['match_id'] = "1234"
test_data['Date'] = "1.1.2001"
test_data['Time'] = "12:01"
test_data['Duration'] = "10.5"
test_data['Win'] = "Win"
test_data['Champion'] = "Renekton"
test_data['Lane_Opponent'] = "Tryndamere"
test_data['CS/min'] = "8.5"
test_data['Kills'] = 4
test_data['Deaths'] = 2
test_data['Assists'] = 5


if __name__ == "__main__":
    # sys.argv = ["streamlit", "run", APP_FILE]
    # stcli.main()
    initialize_database()
    update_database("Lah", "2888", "RGAPI-4b63ddb5-2f6a-4239-9f66-085a2c1e061e")
    pass


