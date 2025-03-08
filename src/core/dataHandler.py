from datetime import datetime

from core.riotAPI import fetch_match_details, fetch_latest_games, fetch_puuid
from core.database import fetch_match_ids, insert_match

def extract_match_data(match_json, puuid):
    data = {}
    data['match_id'] = match_json["metadata"]["matchId"]
    game_creation = match_json["info"]["gameCreation"]
    game_duration = match_json["info"]["gameDuration"]

    game_datetime = datetime.utcfromtimestamp(game_creation / 1000)
    data['Date'] = game_datetime.strftime('%Y-%m-%d')
    data['Time'] = game_datetime.strftime('%H:%M:%S')
    data['Duration'] = f"{game_duration // 60}:{game_duration % 60:02d}"

    player_data = next((p for p in match_json["info"]["participants"] if p["puuid"] == puuid), None)
    if not player_data:
        print(f"Player's data not found in match {data['match_id']}")
        return None

    data['Champion'] = player_data["championName"]
    player_lane = player_data["individualPosition"]
    player_cs = player_data["totalMinionsKilled"]
    data['Win'] = 1 if player_data["win"] else 0
    data['CS/min'] = round(player_cs / (game_duration / 60), 2) if game_duration > 0 else 0
    data['Kills'] = player_data["kills"]
    data['Deaths'] = player_data["deaths"]
    data['Assists'] = player_data["assists"]

    opponent_data = next(
        (p for p in match_json["info"]["participants"]
         if p["individualPosition"] == player_lane and p["teamId"] != player_data["teamId"]),
        None
    )
    data['Lane_Opponent'] = opponent_data["championName"] if opponent_data else "Unknown"

    return data

def update_database(game_name, tag_line, api_key):
    puuid = fetch_puuid(game_name, tag_line, api_key)
    match_ids_in_db = fetch_match_ids()
    existing_match_ids = [match_id[0] for match_id in match_ids_in_db]

    latest_matches = fetch_latest_games(puuid, api_key)
    if not latest_matches:
        print("No new matches found.")
        return

    new_match_ids = [m for m in latest_matches if m not in existing_match_ids]
    if not new_match_ids:
        print("No new matches to add.")
        return

    print(f"Fetching {len(new_match_ids)} new matches...")

    new_matches = []
    for match_id in new_match_ids:
        match_json = fetch_match_details(match_id, api_key)
        if match_json:
            extracted_data = extract_match_data(match_json, puuid)
            if extracted_data:
                new_matches.append(extracted_data)

    if not new_matches:
        print("No new match data extracted.")
        return

    for match in new_matches:
        insert_match(match)

    print(f"CSV updated successfully with {len(new_matches)} new matches!")