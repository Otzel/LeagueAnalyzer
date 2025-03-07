import json
import csv
from datetime import datetime

def write_json(matches_json):
    with open("match_data.json", "w", encoding="utf-8") as json_file:
        json.dump(matches_json, json_file, indent=4, ensure_ascii=False)

    print("Json has been saved")


# Load JSON data (assuming it comes from a request or a JSON object)
def process_match_data(match_data):
    csv_file = "match_summary.csv"

    # Open CSV file for writing with semicolon as delimiter
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")  # <-- Semicolon as delimiter

        # Write headers
        writer.writerow(["MatchID", "Date", "Time", "Game Duration", "Win/Loss", "Champion (Lah)",
                         "Lane Opponent Champion", "CS/min (Lah)", "Comment"])

        for match in match_data:
            match_id = match["metadata"]["matchId"]
            game_creation = match["info"]["gameCreation"]
            game_duration = match["info"]["gameDuration"]

            # Convert timestamp to readable date & time
            game_datetime = datetime.utcfromtimestamp(game_creation / 1000)
            game_date = game_datetime.strftime('%Y-%m-%d')
            game_time = game_datetime.strftime('%H:%M:%S')

            # Convert game duration to minutes:seconds format
            minutes = game_duration // 60
            seconds = game_duration % 60
            game_length = f"{minutes}:{seconds:02d}"

            # Find Lah's player data
            lah_puuid = "Y4jhr6e1vWvF6q6Num4oQEgCvVcBkm7hXobkLh9f3L5LM3l_i8YLzUX80MhAHV6feLdi-G13WcDivw"
            lah_data = next((p for p in match["info"]["participants"] if p["puuid"] == lah_puuid), None)

            if not lah_data:
                print(f"Lah's data not found in match {match_id}")
                continue

            lah_champion = lah_data["championName"]
            lah_lane = lah_data["individualPosition"]
            lah_cs = lah_data["totalMinionsKilled"]
            lah_win = "Win" if lah_data["win"] else "Loss"  # <-- Check if Lah won or lost

            # Calculate CS per minute
            cs_per_min = round(lah_cs / minutes, 2) if minutes > 0 else 0

            # Find lane opponent (same lane, opposite team)
            opponent_data = next(
                (p for p in match["info"]["participants"]
                 if p["individualPosition"] == lah_lane and p["teamId"] != lah_data["teamId"]),
                None
            )

            opponent_champion = opponent_data["championName"] if opponent_data else "Unknown"

            # Write row to CSV (last column is empty for manual comments)
            writer.writerow(
                [match_id, game_date, game_time, game_length, lah_win, lah_champion, opponent_champion, cs_per_min, ""])

    print(f"CSV file '{csv_file}' created successfully with semicolon delimiter!")



# import sqlite3
#
# class database():
#     def __init__(self):
#         self.conn = sqlite3.connect('games.db')
#         self.c = self.conn.cursor()
#
#     def create_tables(self):
#         # Create a table to store game data using proper SQLite data types.
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS games (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             date DATE,             -- Expecting date in ISO8601 format (YYYY-MM-DD)
#             win BOOLEAN,         -- Expecting win boolean
#             game_length REAL,
#             cs REAL,
#             early_cs_avg REAL,
#             mid_cs_avg REAL,
#             late_cs_avg REAL
#         );
#         """
#         self.c.execute(create_table_query)
#         self.conn.commit()
#
#     def insert_game(self, game_obj):
#         # Insert a game object into the games table.
#         insert_query = """
#         INSERT INTO games (date, game_length, early_cs_avg, mid_cs_avg, late_cs_avg)
#         VALUES (?, ?, ?, ?, ?);
#         """
#         values = (
#             game_obj.date,
#             game_obj.game_length,
#             game_obj.early_cs_avg,
#             game_obj.mid_cs_avg,
#             game_obj.late_cs_avg
#         )
#         self.c.execute(insert_query, values)
#         self.conn.commit()
#
#     def close(self):
#         self.conn.close()
