import csv
import os
from riotAPI import fetch_match_details, fetch_latest_games
from datetime import datetime

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "match_summary.csv")

# --- Function to Load Existing CSV ---
def load_existing_csv():
    """Load existing CSV if available, else return empty DataFrame."""
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)  # Skip header
            data = list(reader)
        return data
    return []

# --- Function to Extract Relevant Data ---
def extract_match_data(match_json, puuid):
    """Extract required data from a match JSON."""
    match_id = match_json["metadata"]["matchId"]
    game_creation = match_json["info"]["gameCreation"]
    game_duration = match_json["info"]["gameDuration"]

    # Convert timestamp
    game_datetime = datetime.utcfromtimestamp(game_creation / 1000)
    game_date = game_datetime.strftime('%Y-%m-%d')
    game_time = game_datetime.strftime('%H:%M:%S')
    game_length = f"{game_duration // 60}:{game_duration % 60:02d}"

    # Find Lah's match data
    lah_data = next((p for p in match_json["info"]["participants"] if p["puuid"] == puuid), None)
    if not lah_data:
        print(f"Lah's data not found in match {match_id}")
        return None

    lah_champion = lah_data["championName"]
    lah_lane = lah_data["individualPosition"]
    lah_cs = lah_data["totalMinionsKilled"]
    lah_win = "Win" if lah_data["win"] else "Loss"
    cs_per_min = round(lah_cs / (game_duration / 60), 2) if game_duration > 0 else 0
    kills = lah_data["kills"]
    deaths = lah_data["deaths"]
    assists = lah_data["assists"]

    # Find lane opponent (same lane, opposite team)
    opponent_data = next(
        (p for p in match_json["info"]["participants"]
         if p["individualPosition"] == lah_lane and p["teamId"] != lah_data["teamId"]),
        None
    )
    opponent_champion = opponent_data["championName"] if opponent_data else "Unknown"

    return [match_id, game_date, game_time, game_length, lah_win, lah_champion, opponent_champion, cs_per_min, kills,
            deaths, assists, ""]


# --- Function to Update CSV ---
def update_csv(puuid, api_key):
    """Main function to update the CSV with new games."""
    existing_data = load_existing_csv()
    existing_match_ids = {row[0] for row in existing_data}  # Get stored match IDs

    # Fetch latest matches
    latest_matches = fetch_latest_games(puuid, api_key)
    if not latest_matches:
        print("No new matches found.")
        return

    # Determine new matches
    new_match_ids = [m for m in latest_matches if m not in existing_match_ids]
    if not new_match_ids:
        print("No new matches to add.")
        return

    print(f"Fetching {len(new_match_ids)} new matches...")

    new_rows = []
    for match_id in new_match_ids:
        match_json = fetch_match_details(match_id, api_key)
        if match_json:
            extracted_data = extract_match_data(match_json, puuid)
            if extracted_data:
                new_rows.append(extracted_data)

    # If no new data, stop here
    if not new_rows:
        print("No new match data extracted.")
        return

    # Write to CSV (append mode if file exists, else create new file)
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a" if file_exists else "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")

        # Write header if new file
        if not file_exists:
            writer.writerow(["MatchID", "Date", "Time", "Game Duration", "Win/Loss",
                             "Champion (Lah)", "Lane Opponent Champion", "CS/min (Lah)",
                             "Kills", "Deaths", "Assists", "Comment about Lane Opponent", "Comment about Macro"])

        # Append new rows
        writer.writerows(new_rows)

    print(f"CSV updated successfully with {len(new_rows)} new matches!")
