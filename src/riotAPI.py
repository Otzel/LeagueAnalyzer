import requests

API_KEY = "RGAPI-4b63ddb5-2f6a-4239-9f66-085a2c1e061e"  # <-- Replace with your Riot API Key
PUUID = "Y4jhr6e1vWvF6q6Num4oQEgCvVcBkm7hXobkLh9f3L5LM3l_i8YLzUX80MhAHV6feLdi-G13WcDivw"
MATCH_HISTORY_URL = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{PUUID}/ids?start=0&count=100&api_key={API_KEY}"
MATCH_DETAILS_URL = "https://europe.api.riotgames.com/lol/match/v5/matches/{}?api_key=" + API_KEY

# --- Function to Fetch Latest Matches ---
def fetch_latest_games():
    """Fetch match IDs from Riot API."""
    response = requests.get(MATCH_HISTORY_URL)
    if response.status_code != 200:
        print(f"Error fetching match IDs: {response.status_code}")
        return []
    return response.json()


# --- Function to Fetch Match Details ---
def fetch_match_details(match_id):
    """Fetch match details for a given match ID."""
    response = requests.get(MATCH_DETAILS_URL.format(match_id))
    if response.status_code != 200:
        print(f"Error fetching match {match_id}: {response.status_code}")
        return None
    return response.json()
