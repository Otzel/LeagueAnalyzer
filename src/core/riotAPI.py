import requests

BASE_URL = "https://europe.api.riotgames.com"
PUUID_URL = f"{BASE_URL}/riot/account/v1/accounts/by-riot-id/{{}}/{{}}?api_key={{}}"
MATCH_HISTORY_URL = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{{}}/ids?start=0&count=100&api_key={{}}"
MATCH_DETAILS_URL = f"{BASE_URL}/lol/match/v5/matches/{{}}?api_key={{}}"


def fetch_puuid(game_name, tag_line, api_key):
    url = PUUID_URL.format(game_name, tag_line, api_key)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"⚠️ Error fetching PUUID ({response.status_code}): {response.text}")
        return None

    return response.json().get('puuid')


def fetch_latest_games(puuid, api_key, count=100):
    url = MATCH_HISTORY_URL.format(puuid, api_key).replace("count=100", f"count={count}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"⚠️ Error fetching match IDs ({response.status_code}): {response.text}")
        return []

    return response.json()


def fetch_match_details(match_id, api_key):
    url = MATCH_DETAILS_URL.format(match_id, api_key)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"⚠️ Error fetching match {match_id} ({response.status_code}): {response.text}")
        return None

    return response.json()
