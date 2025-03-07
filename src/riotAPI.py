import requests

MATCH_HISTORY_URL_PART1 = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"
MATCH_HISTORY_URL_PART2 = "/ids?start=0&count=100&api_key="
MATCH_DETAILS_URL_PART1 = "https://europe.api.riotgames.com/lol/match/v5/matches/{}?api_key="


# --- Function to Fetch Latest Matches ---
def fetch_latest_games(puuid, api_key):
    """Fetch match IDs from Riot API."""
    response = requests.get(MATCH_HISTORY_URL_PART1 + puuid + MATCH_HISTORY_URL_PART2 + api_key)
    if response.status_code != 200:
        print(f"Error fetching match IDs: {response.status_code}")
        return []
    return response.json()


# --- Function to Fetch Match Details ---
def fetch_match_details(match_id, api_key):
    """Fetch match details for a given match ID."""
    response = requests.get(MATCH_DETAILS_URL_PART1.format(match_id) + api_key)
    if response.status_code != 200:
        print(f"Error fetching match {match_id}: {response.status_code}")
        return None
    return response.json()
